# DemoPandas2.ipynb
from pandas import Series, DataFrame
import pandas as pd

#딕셔너리를 입력
data = {"foreigner":[1,2,3,4,5,6],
        "sratio":[10,20,30,40,50,60],
        "org":[100,200,300,400,500,600],
        "sprice":[1,2,3,4,5,6],
        "private":[10,20,30,40,50,60]
        }
#데이터프레임으로 변환
frame = DataFrame(data=data)
print(frame)
#원하는 컬럼 순서 지정
frame2 = DataFrame(data=data,
        columns=["foreigner", "org", "private", "sprice", "sratio"],
        index=["2026-03-01", "2026-03-02", "2026-03-03", "2026-03-04", "2026-03-05", "2026-03-06"])
print(frame2)

frame2.T

print(frame2)