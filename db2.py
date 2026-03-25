# db2.py
import sqlite3

#영구적으로 파일에 저장
#(raw string notation: 문자열 앞에 r을 붙여서 백슬래시를 이스케이프 문자로 인식하지 않도록 함)
con = sqlite3.connect(r"c:\work\sample.db");
# #영구적으로 파일에 저장(경로 미지정 시 워크 폴더에 저장 됨)
# con = sqlite3.connect("test.db");
#커서객체 리턴
cur = con.cursor();
#테이블 생성
cur.execute("create table PhoneBook (Name text, PhoneNum text);");
#데이터 삽입
cur.execute("insert into PhoneBook values('홍길동', '010-1234-5678');");
#매개변수로 입력
name = "전우치";
phoneNum = "010-9999-8888";
cur.execute("insert into PhoneBook values(?, ?);", (name, phoneNum));
#다중 데이터를 입력
dataList = (('김철수', '010-1111-2222'), ('박영희', '010-3333-4444'),);
cur.executemany("insert into PhoneBook values(?, ?);", dataList);

# #데이터 조회
for row in cur.execute("select * from PhoneBook;"):
    print(row);

#작업 완료
con.commit();

#연결 종료
con.close();