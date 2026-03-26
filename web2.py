# web2.py
#웹크롤링 선언
from bs4 import BeautifulSoup
#웹사이트 요청
import urllib.request
#정규표현식 추가
import re

#파일로 저장(wt: write text)
f = open("clien.txt", "wt", encoding="utf-8")

#페이지 처리
for i in range(0, 10):
    url = "https://www.clien.net/service/board/sold?&od=T31&category=0&po=" + str(i)
    print(url)
    #User-Agent를 조작하는 경우(PC에서 사용하는 크롬 브라우져의 헤더)
    hdr = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

    req = urllib.request.Request(url, headers = hdr)
    data = urllib.request.urlopen(req).read()

    #검색이 용이한 스프 객체
    soup = BeautifulSoup(data, "html.parser")

    lst = soup.find_all("span", attrs={"data-role":"list-title-text"})
    for tag in lst:
        title = tag.text.strip()
        if re.search("아이폰", title):
            print(title)
            f.write(title + "\n") #파일에 쓰기

f.close()
# <span class="subject_fixed" data-role="list-title-text" title="닌텐도 스위치 라이트 그레이 + 타이틀 4종 / 22만원">
# 							닌텐도 스위치 라이트 그레이 + 타이틀 4종 / 22만원
# </span>
