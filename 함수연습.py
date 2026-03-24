# 함수연습.py

#1) 함수를 정의
def setValue(newValue):
    #지역변수
    x = newValue
    print("함수내부:", x)

#2) 함수를 호출
retValue = setValue(3)
print(retValue)

#1) 함수를 정의
def swap(x,y):
    return y,x

#2) 함수를호출
print(swap(3,4))

#함수 내부에서 이름 해석 규칙(LGB)
x = 5
def func(a):
    return a+x

print(func(1))

def func2(a):
    x = 10
    return a+x

print(func2(1))
print(func(1))

# 함수의 기본값
def times(a=10, b=20):
    print(a*b)
    return a*b
times()
times(5)
times(5,6)

#키워드 인자 방식
def connectURI(server, port):
    strURL = "http://" + server + ":" + port
    return strURL

#호출 
print(connectURI("naver.com", "80"))
print(connectURI(port="8080", server="multicom"))

#가변인자
def union(*ar):
    #지역볒수
    result = []
    for item in ar:
        for x in item:
            if x not in result:
                result.append(x)
    return result

#호출
print(union("HAM","EGG"))
print(union("HAM","EGG","SPAM"))

#람다함수 정의
g = lambda x,y:x*y
print(g(3,4))
print(g(5,6))
print( (lambda x:x*x)(3) )
print( dir() )
print( globals() )