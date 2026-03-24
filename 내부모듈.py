#내부모듈.py
import random

print(random.random())
print(random.random())
print(random.uniform(2.0, 5.0))
print(random.uniform(2.0, 5.0))
print([random.randrange(20) for i in range(10)])
print([random.randrange(20) for i in range(10)])
print(random.sample(range(20), 10))
print(random.sample(range(20), 10))
print(random.sample(range(1,46), 6))
lst = list((range(1,46)))
random.shuffle(lst)
print(lst)

#운영체제 정보
#파일 정보
import os
from os.path import *

print("운여에제명:", os.name)
print("현재 작업 디렉토리:", os.getcwd())
print("현재 작업 디렉토리의 파일 목록:", os.listdir())

fileName = "c:\\python313\\python.exe"

if (exists(fileName)):
    print("파일명:", basename(fileName))
    print("디렉토리명:", dirname(fileName))
    print("파일 크기:", getsize(fileName), "bytes")
else:
    print("파일이 존재하지 않습니다.")

import glob
tmp = glob.glob(r"c:\work\*.py")
for t in tmp:
    if "time" in t:
        print(t)
    else:
        print("time이 포함된 파일이 없습니다.")