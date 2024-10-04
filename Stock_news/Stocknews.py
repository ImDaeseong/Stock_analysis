import requests
from bs4 import BeautifulSoup


class Stocknews:
    def __init__(self, stock_code):
        self.stock_code = stock_code
        self.base_url = f'https://finance.naver.com/item/news_news.naver?code={stock_code}&page=&sm=title_entity_id.basic&clusterId='
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.124 Safari/537.36 '
        }

    def get_Stock_news(self):
        try:
            # print(self.base_url)
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"데이터 확인 실패: {e}")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')

        rows = soup.select('table.type5 tr:not(.relation_tit):not(.relation_lst)')

        news_list = []
        for row in rows:
            title_elem = row.select_one('td.title a.tit')
            if title_elem:
                title = title_elem.text.strip()
                link = "https://finance.naver.com" + title_elem['href']

                info_elem = row.select_one('td.info')
                date_elem = row.select_one('td.date')

                info = info_elem.text.strip() if info_elem else "N/A"
                date = date_elem.text.strip() if date_elem else "N/A"

                news_list.append({
                    "title": title,
                    "link": link,
                    "source": info,
                    "date": date
                })

        return news_list
