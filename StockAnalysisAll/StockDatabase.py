import sqlite3


class StockDatabase:

    def __init__(self, db_name='stock_data.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        # self.drop_table()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                코드 TEXT,
                날짜 TEXT,
                종가 TEXT,
                전일비 TEXT,
                시가 TEXT,
                고가 TEXT,
                저가 TEXT,
                거래량 TEXT
            )
        ''')
        self.conn.commit()

    def drop_table(self):
        self.cursor.execute('DROP TABLE IF EXISTS stock_data')
        self.conn.commit()

    def insert_data(self, stock_code, data):
        for item in data:
            # 중복 확인
            self.cursor.execute('''
                        SELECT 1 FROM stock_data WHERE 코드 = ? AND 날짜 = ?
                    ''', (stock_code, item['날짜']))

            # 데이터 삽입
            if not self.cursor.fetchone():
                self.cursor.execute('''
                    INSERT INTO stock_data (코드, 날짜, 종가, 전일비, 시가, 고가, 저가, 거래량)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (stock_code, item['날짜'], item['종가'], item['전일비'], item['시가'], item['고가'], item['저가'], item['거래량']))
        self.conn.commit()

    def select_data(self, stock_code):
        self.cursor.execute('SELECT * FROM stock_data WHERE 코드 = ? ORDER BY 날짜 DESC', (stock_code,))
        rows = self.cursor.fetchall()
        return rows

    def delete_data(self, stock_code):
        self.cursor.execute('DELETE FROM stock_data WHERE 코드 = ?', (stock_code,))
        self.conn.commit()

    def count_data(self, stock_code):
        self.cursor.execute('SELECT COUNT(*) FROM stock_data WHERE 코드 = ?', (stock_code,))
        count = self.cursor.fetchone()[0]
        return count

    def close(self):
        self.conn.close()
