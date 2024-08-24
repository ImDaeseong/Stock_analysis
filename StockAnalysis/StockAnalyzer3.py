import sqlite3
import pandas as pd


class StockAnalyzer3:
    def __init__(self, db_name='stock_data.db'):
        self.db_name = db_name

    def load_data(self, stock_code):
        conn = sqlite3.connect(self.db_name)
        query = 'SELECT 날짜, 종가 FROM stock_data WHERE 코드 = ? ORDER BY 날짜 DESC'
        df = pd.read_sql_query(query, conn, params=(stock_code,))
        conn.close()

        # '종가' 컬럼을 숫자로 변환 (천 단위 구분 기호 제거)
        df['종가'] = df['종가'].str.replace(',', '').astype(float)

        # '날짜' 컬럼을 날짜 형식으로 변환
        df['날짜'] = pd.to_datetime(df['날짜'], format='%Y.%m.%d')

        return df

    def analyze_Data(self, stock_code, window=20, num_std_dev=2):
        df = self.load_data(stock_code)

        # 현재 날짜 기준으로 최근 2개월(약 60일) 데이터 필터링
        end_date = df['날짜'].max()
        start_date = end_date - pd.DateOffset(days=60)
        df = df[(df['날짜'] >= start_date) & (df['날짜'] <= end_date)]

        # Bollinger Bands 계산
        df['SMA'] = df['종가'].rolling(window=window, min_periods=1).mean()
        df['Std_Dev'] = df['종가'].rolling(window=window, min_periods=1).std()
        df['Upper_Band'] = df['SMA'] + (df['Std_Dev'] * num_std_dev)
        df['Lower_Band'] = df['SMA'] - (df['Std_Dev'] * num_std_dev)

        # 과매수 및 과매도 신호 생성
        df['Signal'] = ''
        df.loc[df['종가'] > df['Upper_Band'], 'Signal'] = '과매수'
        df.loc[df['종가'] < df['Lower_Band'], 'Signal'] = '과매도'

        # 신호가 있는 경우만 필터링
        df_signals = df[df['Signal'] != '']

        return df_signals if not df_signals.empty else pd.DataFrame()  # 빈 데이터프레임 반환
