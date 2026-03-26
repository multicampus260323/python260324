import sys
import requests
from bs4 import BeautifulSoup
import time
from openpyxl import Workbook
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QProgressBar, QMessageBox, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import QThread, pyqtSignal

class CrawlerWorker(QThread):
    progress = pyqtSignal(int)  # 진행 상황 (0-100)
    status = pyqtSignal(str)    # 상태 메시지
    finished_signal = pyqtSignal(list)  # 완료 시 데이터

    def run(self):
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://finance.naver.com/sise/sise_index.naver?code=KPI200",
        }

        result = []
        total_pages = 20
        for page in range(1, total_pages + 1):
            url = f"https://finance.naver.com/sise/entryJongmok.naver?type=KPI200&page={page}"
            try:
                resp = requests.get(url, headers=headers, timeout=30)
                resp.raise_for_status()

                soup = BeautifulSoup(resp.text, "html.parser")
                table = soup.select_one("div.box_type_m table.type_1")
                if table is None:
                    self.status.emit(f"페이지 {page}: 테이블을 찾을 수 없습니다.")
                    continue

                # 데이터 행만 필터링
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

                self.status.emit(f"페이지 {page}/{total_pages} 완료")
                self.progress.emit(int(page / total_pages * 100))

            except Exception as e:
                self.status.emit(f"페이지 {page} 오류: {str(e)}")

            time.sleep(0.2)  # 딜레이

        self.finished_signal.emit(result)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("네이버 코스피200 크롤러")
        self.setGeometry(300, 300, 800, 600)  # 크기 늘림

        layout = QVBoxLayout()

        self.label = QLabel("크롤링을 시작하려면 버튼을 클릭하세요.")
        layout.addWidget(self.label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

        self.start_button = QPushButton("크롤링 시작")
        self.start_button.clicked.connect(self.start_crawling)
        layout.addWidget(self.start_button)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["순위", "종목명", "현재가", "전일비", "등락률", "거래량", "거래대금(백만)", "시가총액(억)"])
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.worker = None

    def start_crawling(self):
        self.start_button.setEnabled(False)
        self.label.setText("크롤링 중...")
        self.progress_bar.setValue(0)

        self.worker = CrawlerWorker()
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.status.connect(self.label.setText)
        self.worker.finished_signal.connect(self.on_finished)
        self.worker.start()

    def on_finished(self, result):
        # 엑셀 저장
        wb = Workbook()
        ws = wb.active
        ws.title = "KOSPI200"

        ws.append(["순위", "종목명", "현재가", "전일비", "등락률", "거래량", "거래대금(백만)", "시가총액(억)"])

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

        filename = f"kospi200_{time.strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
        wb.save(filename)

        # GUI 테이블에 데이터 표시
        self.table.setRowCount(len(result))
        for i, row in enumerate(result):
            self.table.setItem(i, 0, QTableWidgetItem(str(row["순위"])))
            self.table.setItem(i, 1, QTableWidgetItem(row["종목명"]))
            self.table.setItem(i, 2, QTableWidgetItem(row["현재가"]))
            self.table.setItem(i, 3, QTableWidgetItem(row["전일비"]))
            self.table.setItem(i, 4, QTableWidgetItem(row["등락률"]))
            self.table.setItem(i, 5, QTableWidgetItem(row["거래량"]))
            self.table.setItem(i, 6, QTableWidgetItem(row["거래대금(백만)"]))
            self.table.setItem(i, 7, QTableWidgetItem(row["시가총액(억)"]))

        self.label.setText(f"크롤링 완료! {filename}에 저장되었습니다.")
        self.start_button.setEnabled(True)

        QMessageBox.information(self, "완료", f"총 {len(result)}개의 데이터를 엑셀 파일과 GUI 테이블에 표시했습니다.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())