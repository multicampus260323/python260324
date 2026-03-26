# DemoForm2.py
# DemoForm2.ui(화면단) + DemoForm2.py(로직단)
import sys
#수정
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
#웹크롤링 선언
from bs4 import BeautifulSoup
#웹사이트 요청
import urllib.request
#정규표현식 추가
import re

#디자인 파일 로딩(DemoForm2.ui)
form_class = uic.loadUiType("DemoForm2.ui")[0]

#DemoFOrm 클래스 정의(QMainWindow,form_class 상속)
class DemoForm(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self) #화면단과 로직단 연결
        self.label.setText("Hello PyQt6") #화면단의 label에 텍스트 설정
    #슬롯 메서드 추가
    def firstClick(self):

        #파일로 저장(wt: write text)
        f = open("clien.txt", "wt", encoding="utf-8")
        #페이징 처리(1~10페이지)
        for i in range(0, 10):
            url = "https://www.clien.net/service/board/sold?&od=T31&category=0&po=" + str(i)
            print(url)
            #User-Agent를 조작하는 경우(PC에서 사용하는 크롬 브라우져의 헤더)
            hdr = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
            #리퀘스트 설정 및 웹사이트 요청
            req = urllib.request.Request(url, headers = hdr)
            data = urllib.request.urlopen(req).read()
            #검색이 용이한 스프 객체
            soup = BeautifulSoup(data, "html.parser")
            #검색 대상 태그 찾기
            lst = soup.find_all("span", attrs={"data-role":"list-title-text"})
            for tag in lst:
                title = tag.text.strip()
                if re.search("아이폰", title):
                    print(title)
                    f.write(title + "\n") #파일에 쓰기
        f.close()
        self.label.setText("클리앙 중고장터 크롤링 완료!")
    def secondClick(self):
        self.label.setText("두 번째 버튼 클릭")
    def thirdClick(self):
        self.label.setText("세 번째 버튼 클릭")

#진입점 체크
if __name__ == "__main__":
    app = QApplication(sys.argv) #QApplication 객체 생성
    demo = DemoForm() #DemoForm 객체 생성
    demo.show() #화면 표시
    sys.exit(app.exec()) #이벤트 루프 실행
