import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


class StockDataCollection:

    def __init__(self, stock_code):
        self.stock_code = stock_code
        self.base_url = f"https://finance.naver.com/item/sise_day.nhn?code={stock_code}&page="
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.124 Safari/537.36 '
        }
        self.end_date = datetime.today()
        self.start_date = self.end_date - timedelta(days=60)  # 최근 2개월

    def getTotalpages(self):

        response = requests.get(self.base_url + '1', headers=self.headers)
        if response.status_code != 200:
            print(f"데이터 가져오기 실패: {response.status_code}")
            return 0

        soup = BeautifulSoup(response.content, 'html.parser')

        # '맨뒤' 버튼을 찾아서 마지막 페이지 번호를 추출
        paging_td = soup.find('td', class_='pgRR')
        if paging_td:
            last_page_link = paging_td.find('a')['href']
            last_page_number = last_page_link.split('=')[-1]  # URL에서 페이지 번호를 추출
            return int(last_page_number)
        return 0

    def getSelectpages(self, page):

        response = requests.get(self.base_url + str(page), headers=self.headers)
        if response.status_code != 200:
            print(f"데이터 가져오기 실패: 상태 코드 {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='type2')
        rows = table.find_all('tr')[2:]  # 헤더 행을 스킵

        data = []
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 7:
                date = cols[0].get_text(strip=True)
                close = cols[1].get_text(strip=True)
                change = cols[2].get_text(strip=True)
                open_ = cols[3].get_text(strip=True)
                high = cols[4].get_text(strip=True)
                low = cols[5].get_text(strip=True)
                volume = cols[6].get_text(strip=True)

                # 빈 데이터 체크
                if any([date, close, change, open_, high, low, volume]):
                    data.append({
                        '날짜': date,
                        '종가': close,
                        '전일비': change,
                        '시가': open_,
                        '고가': high,
                        '저가': low,
                        '거래량': volume
                    })
        return data

    def getAllPages(self):

        last_page = self.getTotalpages()
        all_data = []

        for page in range(1, last_page + 1):
            print(f"페이지 {page} 데이터를 수집 중...")
            page_data = self.getSelectpages(page)

            # 날짜 필터링
            filtered_data = [entry for entry in page_data if
                             self.start_date <= datetime.strptime(entry['날짜'], '%Y.%m.%d') <= self.end_date]

            all_data.extend(page_data)

            # 요청 사이에 2초 지연을 추가
            # time.sleep(2)

            # 최근 2개월 데이터만 수집
            if len(filtered_data) > 0 and datetime.strptime(filtered_data[-1]['날짜'], '%Y.%m.%d') < self.start_date:
                break

        return all_data
