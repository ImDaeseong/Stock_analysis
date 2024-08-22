import requests
import json
from bs4 import BeautifulSoup


class StockDataCollection:
    def __init__(self, stock_code):
        self.stock_code = stock_code
        self.base_url = f"https://finance.naver.com/item/sise_day.nhn?code={stock_code}"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.124 Safari/537.36 '
        }

    def get_current_price_info(self):
        try:
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"데이터 확인 실패: {e}")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='type2')
        rows = table.find_all('tr')[2:]

        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 7:
                date = cols[0].get_text(strip=True)
                close = cols[1].get_text(strip=True)
                open_ = cols[3].get_text(strip=True)
                high = cols[4].get_text(strip=True)
                low = cols[5].get_text(strip=True)

                # 유효 데이터 체크
                if all([date, close, open_, high, low]):
                    return {
                        '날짜': date,
                        '종가': close,
                        '시가': open_,
                        '고가': high,
                        '저가': low
                    }

        print("현재 데이터 찾기 실패")
        return None


class JSONSaver:
    def __init__(self, filename='stock_data.json'):
        self.filename = filename

    def save(self, data):
        try:
            with open(self.filename, 'w') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"{self.filename}에 저장 실패: {e}")
