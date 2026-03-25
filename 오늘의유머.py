# web2.py
#웹크롤링 선언
from bs4 import BeautifulSoup
#웹사이트 요청
import urllib.request
#정규표현식 추가
import re

#파일로 저장(wt: write text)
f = open("todayHumor.txt", "wt", encoding="utf-8")

#페이지 처리
for i in range(1, 11):
    url = "https://www.todayhumor.co.kr/board/list.php?table=bestofbest&page=" + str(i)
    print(url)
    #User-Agent를 조작하는 경우(PC에서 사용하는 크롬 브라우져의 헤더)
    # hdr = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
    hdr = {'User-agent':'abcd'}

    req = urllib.request.Request(url, headers = hdr)
    data = urllib.request.urlopen(req).read()

    #검색이 용이한 스프 객체
    soup = BeautifulSoup(data, "html.parser")
    #필요한 태그만 필터링
    lst = soup.find_all("td", attrs={"class":"subject"})
    for tag in lst:
        title = tag.find("a").text.strip()
        if re.search("부", title):
            print(title)
            f.write(title + "\n") #파일에 쓰기

f.close()
# <td class="subject">
#   <a href="/board/view.php?table=bestofbest&amp;no=482478&amp;s_no=482478&amp;page=1" target="_top">굿뉴스</a>
#   <span class="list_memo_count_span"> [5]</span>
#   <span style="margin-left:4px;">
#       <img src="//www.todayhumor.co.kr/board/images/list_icon_photo.gif" style="vertical-align:middle; margin-bottom:1px;">
#   </span>
#   <img src="//www.todayhumor.co.kr/board/images/list_icon_shovel.gif?2" alt="펌글" style="margin-right:3px;top:2px;position:relative">
# </td>
