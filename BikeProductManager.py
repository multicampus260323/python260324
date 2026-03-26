import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt

class BikeProductManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("자전거 용품 관리")
        self.setGeometry(100, 100, 800, 600)

        # 데이터베이스 초기화
        self.init_db()

        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 레이아웃
        layout = QVBoxLayout(central_widget)

        # 입력 섹션
        input_layout = QHBoxLayout()

        self.name_label = QLabel("이름:")
        self.name_edit = QLineEdit()
        self.price_label = QLabel("가격:")
        self.price_edit = QLineEdit()

        self.add_button = QPushButton("입력")
        self.update_button = QPushButton("수정")
        self.delete_button = QPushButton("삭제")
        self.search_button = QPushButton("검색")

        input_layout.addWidget(self.name_label)
        input_layout.addWidget(self.name_edit)
        input_layout.addWidget(self.price_label)
        input_layout.addWidget(self.price_edit)
        input_layout.addWidget(self.add_button)
        input_layout.addWidget(self.update_button)
        input_layout.addWidget(self.delete_button)
        input_layout.addWidget(self.search_button)

        layout.addLayout(input_layout)

        # 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "이름", "가격"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        # 버튼 연결
        self.add_button.clicked.connect(self.add_product)
        self.update_button.clicked.connect(self.update_product)
        self.delete_button.clicked.connect(self.delete_product)
        self.search_button.clicked.connect(self.search_product)

        # 테이블 선택 시 입력 필드 채우기
        self.table.itemSelectionChanged.connect(self.on_table_selection_changed)

        # 초기 데이터 로드
        self.load_products()

    def init_db(self):
        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS MyProduct (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT NOT NULL,
                PRICE REAL NOT NULL
            )
        ''')
        self.conn.commit()

    def load_products(self, search_term=None):
        if search_term:
            self.cursor.execute("SELECT * FROM MyProduct WHERE NAME LIKE ?", ('%' + search_term + '%',))
        else:
            self.cursor.execute("SELECT * FROM MyProduct")
        rows = self.cursor.fetchall()
        self.table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def add_product(self):
        name = self.name_edit.text().strip()
        price_text = self.price_edit.text().strip()
        if not name or not price_text:
            QMessageBox.warning(self, "입력 오류", "이름과 가격을 모두 입력하세요.")
            return
        try:
            price = float(price_text)
        except ValueError:
            QMessageBox.warning(self, "입력 오류", "가격은 숫자로 입력하세요.")
            return

        self.cursor.execute("INSERT INTO MyProduct (NAME, PRICE) VALUES (?, ?)", (name, price))
        self.conn.commit()
        self.load_products()
        self.clear_inputs()

    def update_product(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "선택 오류", "수정할 항목을 선택하세요.")
            return

        id_item = self.table.item(selected_row, 0)
        if not id_item:
            return
        product_id = int(id_item.text())

        name = self.name_edit.text().strip()
        price_text = self.price_edit.text().strip()
        if not name or not price_text:
            QMessageBox.warning(self, "입력 오류", "이름과 가격을 모두 입력하세요.")
            return
        try:
            price = float(price_text)
        except ValueError:
            QMessageBox.warning(self, "입력 오류", "가격은 숫자로 입력하세요.")
            return

        self.cursor.execute("UPDATE MyProduct SET NAME = ?, PRICE = ? WHERE ID = ?", (name, price, product_id))
        self.conn.commit()
        self.load_products()
        self.clear_inputs()

    def delete_product(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "선택 오류", "삭제할 항목을 선택하세요.")
            return

        id_item = self.table.item(selected_row, 0)
        if not id_item:
            return
        product_id = int(id_item.text())

        reply = QMessageBox.question(self, "삭제 확인", "정말로 삭제하시겠습니까?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.cursor.execute("DELETE FROM MyProduct WHERE ID = ?", (product_id,))
            self.conn.commit()
            self.load_products()
            self.clear_inputs()

    def search_product(self):
        search_term = self.name_edit.text().strip()
        self.load_products(search_term)

    def on_table_selection_changed(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            name_item = self.table.item(selected_row, 1)
            price_item = self.table.item(selected_row, 2)
            if name_item and price_item:
                self.name_edit.setText(name_item.text())
                self.price_edit.setText(price_item.text())

    def clear_inputs(self):
        self.name_edit.clear()
        self.price_edit.clear()

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BikeProductManager()
    window.show()
    sys.exit(app.exec())