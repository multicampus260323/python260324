import requests
from bs4 import BeautifulSoup
import time
from openpyxl import Workbook

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://finance.naver.com/sise/sise_index.naver?code=KPI200",
}

result = []
for page in range(1, 21):  # 1부터 20페이지까지
    url = f"https://finance.naver.com/sise/entryJongmok.naver?type=KPI200&page={page}"
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.select_one("div.box_type_m table.type_1")
    if table is None:
        print(f"페이지 {page}: 편입종목상위 테이블을 찾을 수 없습니다.")
        continue

    # 데이터 행만 필터링 (헤더와 빈 행 제외)
    data_rows = [tr for tr in table.select("tr") if len(tr.select("td")) == 7]
    for index, tr in enumerate(data_rows):
        tds = tr.select("td")
        rank = (page - 1) * 10 + (index + 1)
        result.append({
            "순위": rank,
            "종목명": tds[0].get_text(strip=True),
            "현재가": tds[1].get_text(strip=True),
            "전일비": tds[2].get_text(strip=True),
            "등락률": tds[3].get_text(strip=True),
            "거래량": tds[4].get_text(strip=True),
            "거래대금(백만)": tds[5].get_text(strip=True),
            "시가총액(억)": tds[6].get_text(strip=True),
        })

    time.sleep(0.2)  # 서버 부하 방지를 위한 딜레이

# 엑셀 파일로 저장
wb = Workbook()
ws = wb.active
ws.title = "KOSPI200"

# 헤더 추가
ws.append(["순위", "종목명", "현재가", "전일비", "등락률", "거래량", "거래대금(백만)", "시가총액(억)"])

# 데이터 추가
for row in result:
    ws.append([
        row["순위"],
        row["종목명"],
        row["현재가"],
        row["전일비"],
        row["등락률"],
        row["거래량"],
        row["거래대금(백만)"],
        row["시가총액(억)"],
    ])
    print(result + "\n")

wb.save("kospi200.xlsx")
print("크롤링 데이터가 kospi200.xlsx 파일로 저장되었습니다.")