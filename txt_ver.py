from pdfrw import *
import sys
import os



# 페이지 사이즈 계산
def calculate_size(source):

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
def filename_maker(string):
    index = string.find('.')

    return string[0:index]


def pdf_checker(string):

    # 파일명에 .pdf가 포함되어있을때
    if string.find('.pdf') != -1:
        return string

    # 파일명에 .pdf가 없을때
    else:
        string = string + '.pdf'

        return string

# update.txt 파일을 통해 변환 시도할 경우, \n 기호때문에 문제 발생. \n기호 제거 필요.
def enter_remover(src):

    src_len = len(src)
    if src[src_len-1:src_len] == '\n':
        src = src[0:src_len-1]

    return src




# 여기부터 main 함수 

txt = open("update.txt", "rt")

while True:
    src = txt.readline()

    # while문 탈출조건
    if not src:
        break

    src = enter_remover(src)
    src = pdf_checker(src)
    print("{}파일 변환을 시작합니다.".format(src))

# 작성 시작
    output = PdfWriter()
    src_pdf = PdfReader(src)
    total_page = len(src_pdf.pages)
    total_count = get_total_count(total_page)

# blank page 만들기
    blank = PageMerge()
    blank.mbox = [0, 0, calculate_size(src_pdf)[0], calculate_size(src_pdf)[1]]
    blank = blank.render()

    count = 1

    for page in src_pdf.pages:
        output.addpage(page)

        if count % 4 == 2 or count % 4 == 0:
            if total_count % 2 == 0 and count == total_count:
                break

            output.addpage(blank)
            output.addpage(blank)

        count += 1

    filename = filename_maker(src)
    output.write(filename+'_빈칸.pdf')

    print("{}파일 생성완료".format(filename+'_빈칸.pdf'))


txt.close()
print("모든 작업이 완료되었습니다.")
