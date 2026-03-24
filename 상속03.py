# -----------------------------------------------
# 1) 기본 Person 클래스 정의
# -----------------------------------------------

class Person:
    def __init__(self, id, name):
        # id는 사람을 구별하는 번호예요.
        # name은 사람 이름이에요.
        self.id = id
        self.name = name

    def printInfo(self):
        # 이 함수는 사람의 정보를 화면에 보여줘요.
        print("== Person 정보 ==")
        print("ID:", self.id)
        print("이름:", self.name)
        print("---------------")

# -----------------------------------------------
# 2) Person에서 상속받아 Manager 만들기 (title 추가)
# -----------------------------------------------

class Manager(Person):
    def __init__(self, id, name, title):
        # 부모(Person)의 id, name을 먼저 초기화해요.
        super().__init__(id, name)
        # title은 관리자 직책(예: 팀장) 정보예요.
        self.title = title

    def printInfo(self):
        # super().printInfo()로 Person 데이터를 먼저 보여주고
        # 추가로 관리자 직책을 보여줘요.
        super().printInfo()
        print("직책:", self.title)
        print("===============")

# -----------------------------------------------
# 3) Person에서 상속받아 Employee 만들기 (skill 추가)
# -----------------------------------------------

class Employee(Person):
    def __init__(self, id, name, skill):
        # 부모(Person) 설정 먼저
        super().__init__(id, name)
        # skill은 직원이 잘하는 기술(예: 코딩, 디자인)이에요.
        self.skill = skill

    def printInfo(self):
        # Person 정보 + 추가 skill 정보 출력
        super().printInfo()
        print("기술:", self.skill)
        print("===============")

# -----------------------------------------------
# 4) 테스트 코드 10개 (assert + 출력)
# -----------------------------------------------

def run_tests():
    # 테스트 1~3: Person
    p1 = Person(1, "철수")
    assert p1.id == 1
    assert p1.name == "철수"
    p1.printInfo()

    p2 = Person(2, "영희")
    assert p2.id == 2
    assert p2.name == "영희"
    p2.printInfo()

    p3 = Person(3, "민수")
    assert p3.id == 3
    assert p3.name == "민수"
    p3.printInfo()

    # 테스트 4~6: Manager
    m1 = Manager(11, "지훈", "부장")
    assert m1.id == 11
    assert m1.name == "지훈"
    assert m1.title == "부장"
    m1.printInfo()

    m2 = Manager(12, "소연", "이사")
    assert m2.id == 12
    assert m2.name == "소연"
    assert m2.title == "이사"
    m2.printInfo()

    # Manager에서 Person 메서드도 동일하게 동작하는지 확인
    m3 = Manager(13, "민지", "과장")
    assert isinstance(m3, Person)
    m3.printInfo()

    # 테스트 7~9: Employee
    e1 = Employee(21, "영수", "파이썬")
    assert e1.id == 21
    assert e1.name == "영수"
    assert e1.skill == "파이썬"
    e1.printInfo()

    e2 = Employee(22, "수지", "데이터분석")
    assert e2.id == 22
    assert e2.name == "수지"
    assert e2.skill == "데이터분석"
    e2.printInfo()

    e3 = Employee(23, "훈이", "게임제작")
    assert e3.id == 23
    assert e3.name == "훈이"
    assert e3.skill == "게임제작"
    e3.printInfo()

    # 테스트 10: 상속 관계 체크
    assert isinstance(e3, Person)
    assert isinstance(m3, Person)

    print("모든 테스트 통과!")

# 실제 실행
if __name__ == "__main__":
    run_tests()