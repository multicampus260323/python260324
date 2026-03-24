#부모 클래스
class Person:
    def __init__(self, name, phoneNumber):
        self.name = name
        self.phoneNumber = phoneNumber

    def printInfo(self):
        print("Info(Name:{0}, Phone Number: {1})".format(self.name, self.phoneNumber))

#자식 클래스
class Student(Person):
    #상속 받고 재정의
    def __init__(self, name, phoneNumber, subject, studentID):
        super().__init__(name, phoneNumber) # 부모 클래스의 초기화 메서드 호출
        self.subject = subject
        self.studentID = studentID
    #상속 받고 재정의
    def printInfo(self):
        print("Info(Name:{0}, Phone Number: {1}, Subject: {2}, Student ID: {3})".format(self.name, self.phoneNumber, self.subject, self.studentID ))


p = Person("전우치", "010-222-1234")
s = Student("이순신", "010-111-1234", "컴공", "991122")
p.printInfo()
s.printInfo()