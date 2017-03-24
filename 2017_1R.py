from pdfrw import *
import os


# 페이지 사이즈 계산
def calculate_size(source):

    #rotate_90 체크 : 석준희교수님 강의안 Lecture 00 파일때문에 만든 if문 원래는 else 부분만 있었음.
    if source.pages[0]['/Rotate'] == '90':
        raw_size_x = source.pages[0]['/MediaBox'][3]
        raw_size_y = source.pages[0]['/MediaBox'][2]

    else:
        raw_size_x = source.pages[0]['/MediaBox'][2]
        raw_size_y = source.pages[0]['/MediaBox'][3]


    # 사이즈가 정수가 아닐경우 문제 발생. 소수점 제거를 위한 if문 두개
    if raw_size_x.find('.') != -1:
        raw_size_x = raw_size_x[0:raw_size_x.find('.')]

    if raw_size_y.find('.') != -1:
        raw_size_y = raw_size_y[0:raw_size_y.find('.')]


    page_size_x = int(raw_size_x)
    page_size_y = int(raw_size_y)

    return (page_size_x, page_size_y)


def get_total_count(total_page):
    if total_page % 2 == 1:
        return total_page * 2 - 1

    else:
        return total_page * 2 - 2


# .pdf 부분은 잘라내기 위한 함수.
def fileext_strip(string):
    index = string.find('.')

    return string[0:index]


def fileext_checker(string):

    # 파일명에 .pdf가 포함되어있을때
    if string.find('.pdf') != -1:
        return string

    # 파일명에 .pdf가 없을때
    else:
        string = string + '.pdf'

        return string


def get_pathlist():
    #pathlist = ['객체지향프로그래밍', '데이터베이스', '반도체공학', '종합설계']
    pathlist = ['객체지향프로그래밍', '데이터베이스', '반도체공학']
    #pathlist = ['객체지향프로그래밍']
    return pathlist


# blank page 공식(pdf마다 규격이 달라서... 파일마다 호출해야함)
def make_blank_page(src_pdf):
    blank = PageMerge()
    blank.mbox = [0, 0, calculate_size(src_pdf)[0], calculate_size(src_pdf)[1]]
    blank = blank.render()
    return blank


def make_pdf(src):

# 작성 시작
    output = PdfWriter()
    src_pdf = PdfReader(src)
    total_page = len(src_pdf.pages)
    total_count = get_total_count(total_page)

# blank page 만들기
    blank = make_blank_page(src_pdf)

    page_num = 1

    for page in src_pdf.pages:
        output.addpage(page)

        if page_num % 4 == 2 or page_num % 4 == 0:
            if total_count % 2 == 0 and page_num == total_count:
                break

            output.addpage(blank)
            output.addpage(blank)

        page_num += 1

    filename = fileext_strip(src)
    output.write(filename+'_BLANK.pdf')

    print("{}파일 생성완료".format(filename+'_BLANK.pdf'))


def already_exist(src, filelist):

    # 이미 _BLANK 파일이 존재할경우 && src가 현재 _BLANK 파일일경우
    if src.find('_BLANK') != -1:
        print("{} already exist".format(src))
        return True

    # 이미 _BLANK 파일이 존재할경우 && src가 현재 일반 파일일경우
    else:
        src_len = len(src)

        if (src[0:src_len-4]+'_BLANK.pdf' in filelist):
            #print("{} already exist".format(src))
            return True

    # 존재하지 않을경우 (False를 리턴함으로서, _BLANK 파일을 생성하도록 신호를 주는것)
    return False


def is_pdf(filelist):
    for filename in filelist:
        # 확장자에 .pdf가 없다면(.pptx같은거), 리스트에서 제거한다
        if filename.find('.pdf') == -1:
            filelist.remove(filename)


def delete_checker(filename):
    # _빈칸 확장자가 붙어있나 체크. -1이 아니면 있다는 소리임!
    if filename.find('_빈칸') != -1:
        return True

    if filename.find('_BLANK') != -1:
        return True

    else:
        return False


def create():
    pathlist = get_pathlist()

    for path in pathlist:
        print("="*50)
        print("\'{}\'폴더에 대한 작업을 시작합니다.".format(path))
        print("="*50)


        # 디렉토리를 바꿔준다. (예를들면 데이터베이스 폴더로) 그리고 그 디렉토리의 파일명을 싹 리스트화시킨다.
        os.chdir(path)
        filelist = os.listdir()
        is_pdf(filelist)


        # 해당 폴더에 대해 작업시작
        for src in filelist:

            # 본격적인 파일생성 이전에, 예외 처리 2단계를 거침
            # 1. 이미 해당 파일이 존재하는 경우
            if already_exist(src, filelist) is True:
                continue

            # 2. 예외에 해당하는 경우
            if src in exception_list:
                continue

            src = fileext_checker(src)
            make_pdf(src)


        print("\n\'{}\'폴더에 대한 작업이 완료되었습니다.\n".format(path))
        os.chdir('..')


    print("모든 작업이 완료되었습니다.")


def delete():
    pathlist = get_pathlist()

    for path in pathlist:
        print("="*50)
        print("\'{}\'폴더에 대한 작업을 시작합니다.".format(path))
        print("="*50)
        
        os.chdir(path)
        filelist = os.listdir()

        for filename in filelist:
            if delete_checker(filename) is True:
                os.remove(filename)
                print("{}를 삭제하였습니다".format(filename))

        print("\n\'{}\'폴더에 대한 작업이 완료되었습니다.\n".format(path))
        os.chdir('..')

    print("작업이 완료되었습니다.")


#============main funciton==============#
exception_list = []

if __name__ == "__main__":

    while True:
        print("="*50+"\npdf program version 1.0\n"+"="*50)
        print("\n0 : exit")
        print("1 : create()")
        print("2 : delete()")
        print("3 : change pathlist\n")

        program = input("수행할 명령어를 입력하세요 : ")

        if program == '1':
            print("빈페이지 만들기 작업을 시작합니다.\n\n")
            create()

        elif program == '2':
            print("_BLANK 또는 _빈칸 확장자 파일들을 제거합니다. \n\n")
            delete()


        elif program == '0':
            print("프로그램을 종료합니다\n")
            break

        else:
            break
