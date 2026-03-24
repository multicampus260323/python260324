# 상속02.py
# Person클래스를 정의하는데 id, name 변수가 있고
# printInfo()라는 메서드로 해당 정보를 출력
class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def printInfo(self):
        print("Info(ID:{0}, Name: {1})".format(self.id, self.name)) 
    
# 해당 클래스의 인스턴스를 생성
p = Person(100, "전우치")
p.printInfo()