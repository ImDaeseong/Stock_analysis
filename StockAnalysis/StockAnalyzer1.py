import numpy as np
import sqlite3
import pandas as pd


class StockAnalyzer1:
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

    def set_averages(self, df, short_window=5, long_window=20):
        # 단기 이동 평균 계산
        df['단기_이동평균'] = df['종가'].rolling(window=short_window, min_periods=1).mean()

        # 장기 이동 평균 계산
        df['장기_이동평균'] = df['종가'].rolling(window=long_window, min_periods=1).mean()

        return df

    def check_signals(self, df):
        # 초기 신호 설정
        df['신호'] = 0

        # 매수 신호 및 매도 신호 생성
        df['신호'] = np.where(df['단기_이동평균'] > df['장기_이동평균'], 1, 0)

        # 신호의 변화 계산 (매수 또는 매도 신호 발생 지점)
        df['위치'] = df['신호'].diff()

        # 매수 신호 (신호가 1로 변하는 지점)
        df['매수_신호'] = np.where(df['위치'] == 1, df['종가'], np.nan)

        # 매도 신호 (신호가 0으로 변하는 지점)
        df['매도_신호'] = np.where(df['위치'] == -1, df['종가'], np.nan)

        return df

    def analyze_Data(self, stock_code):
        df = self.load_data(stock_code)

        # 이동 평균 기간 설정
        short_window = 5
        long_window = 20

        # 이동 평균 계산
        df = self.set_averages(df, short_window, long_window)

        # 매수 및 매도 신호 생성
        df = self.check_signals(df)

        # 현재 날짜 기준으로 최근 20개월(약 400일) 데이터 필터링
        end_date = df['날짜'].max()
        start_date = end_date - pd.DateOffset(months=20)
        df = df[(df['날짜'] >= start_date) & (df['날짜'] <= end_date)]

        # 매수 및 매도 신호가 있는 경우만 필터링
        df_signals = df.dropna(subset=['매수_신호', '매도_신호'])

        # 빈 데이터프레임 반환
        return df_signals if not df_signals.empty else pd.DataFrame()
