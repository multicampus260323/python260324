# db3.py
import sqlite3
import random
import string
from typing import List, Tuple, Optional

class ProductDB:
    def __init__(self, db_path: str = "MyProduct.db"):
        self.db_path = db_path
        self._ensure_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _ensure_table(self):
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Products (
                    productID INTEGER PRIMARY KEY,
                    productName TEXT NOT NULL,
                    productPrice INTEGER NOT NULL
                )
            """)
            conn.commit()

    def insert_product(self, product_id: int, product_name: str, product_price: int):
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT OR REPLACE INTO Products(productID, productName, productPrice) VALUES (?, ?, ?)",
                (product_id, product_name, product_price)
            )
            conn.commit()

    def insert_products_bulk(self, items: List[Tuple[int, str, int]], batch_size: int = 10000):
        with self._connect() as conn:
            cur = conn.cursor()
            for i in range(0, len(items), batch_size):
                cur.executemany(
                    "INSERT OR REPLACE INTO Products(productID, productName, productPrice) VALUES (?, ?, ?)",
                    items[i:i+batch_size]
                )
            conn.commit()

    def update_product(self, product_id: int, product_name: Optional[str] = None, product_price: Optional[int] = None):
        if product_name is None and product_price is None:
            return
        assignments = []
        params = []
        if product_name is not None:
            assignments.append("productName = ?")
            params.append(product_name)
        if product_price is not None:
            assignments.append("productPrice = ?")
            params.append(product_price)
        params.append(product_id)

        sql = f"UPDATE Products SET {', '.join(assignments)} WHERE productID = ?"
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            conn.commit()

    def delete_product(self, product_id: int):
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM Products WHERE productID = ?", (product_id,))
            conn.commit()

    def select_product_by_id(self, product_id: int) -> Optional[Tuple[int, str, int]]:
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT productID, productName, productPrice FROM Products WHERE productID = ?", (product_id,))
            return cur.fetchone()

    def select_all_products(self, limit: Optional[int] = None) -> List[Tuple[int, str, int]]:
        with self._connect() as conn:
            cur = conn.cursor()
            sql = "SELECT productID, productName, productPrice FROM Products"
            if limit != None:
                sql += " LIMIT ?"
                cur.execute(sql, (limit,))
            else:
                cur.execute(sql)
            return cur.fetchall()

def random_product_name(length=10):
    return "제품_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_test_products(count=100000):
    result = []
    for i in range(1, count + 1):
        name = random_product_name(6)
        price = random.randint(10000, 2000000)
        result.append((i, name, price))
    return result

if __name__ == "__main__":
    db = ProductDB("MyProduct.db")

    # 1) 샘플 100,000개 생성 (기존 있으면 overwrite)
    products = generate_test_products(100000)
    db.insert_products_bulk(products)

    # 2) 일부 CRUD 테스트
    db.insert_product(100001, "NEW_PRODUCT", 123456)

    print("100001:", db.select_product_by_id(100001))

    db.update_product(100001, product_price=999999)
    print("100001 업데이트 후:", db.select_product_by_id(100001))

    db.delete_product(100001)
    print("100001 삭제 후:", db.select_product_by_id(100001))

    # 일부 조회
    print("첫 5개 rows:", db.select_all_products(limit=5))

