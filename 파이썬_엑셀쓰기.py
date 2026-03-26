import random
from datetime import datetime, timedelta
from openpyxl import Workbook

# 랜덤 데이터셋 기본값
brands = ["Samsung", "LG", "Apple", "Sony", "Panasonic", "Dell", "HP", "Lenovo", "Asus", "Acer"]
categories = ["스마트폰", "노트북", "태블릿", "TV", "헤드셋", "스피커", "카메라", "공기청정기", "로봇청소기", "모니터"]
product_types = ["프로", "플러스", "맥스", "에어", "스탠다드", "울트라"]

wb = Workbook()
ws = wb.active
ws.title = "Electronics"

# 헤더
ws.append(["ID", "제품명", "브랜드", "카테고리", "가격(원)", "재고", "평점", "출시일"])

base_date = datetime(2018, 1, 1)

for i in range(1, 101):
    brand = random.choice(brands)
    category = random.choice(categories)
    name = f"{brand} {category} {random.choice(product_types)} {random.randint(1, 1000)}"
    price = random.randint(80000, 3500000)
    stock = random.randint(0, 200)
    rating = round(random.uniform(2.5, 5.0), 2)
    release_date = (base_date + timedelta(days=random.randint(0, 2000))).date()

    ws.append([i, name, brand, category, price, stock, rating, release_date])

outfile = "전자제품_100개_데이터.xlsx"
wb.save(outfile)
print(f"완료: {outfile}")