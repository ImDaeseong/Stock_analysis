import json
from Stocknews import Stocknews


def readConfig(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data.get('stock_code')


def readConfigjson(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = [json.loads(line) for line in file]
        return [(entry['company'], entry['code']) for entry in data]


# 종목 뉴스
def stock_news():
    config_path = 'config.json'
    stock_code = readConfig(config_path)

    if not stock_code:
        print("json 파일 읽기 실패")
        exit(1)

    news = Stocknews(stock_code)
    news_list = news.get_Stock_news()
    if not news_list:
        print("뉴스를 찾을 수 없습니다.")
    else:
        for news in news_list:
            print(f"제목: {news['title']}")
            print(f"링크: {news['link']}")
            print(f"출처: {news['source']}")
            print(f"날짜: {news['date']}")
            print("\n")


# 전체 종목 뉴스
def stock_news_all():
    file_path = 'code.json'
    result = readConfigjson(file_path)
    for company, stock_code in result:
        # print(f"회사: {company}, 코드: {stock_code}")
        news = Stocknews(stock_code)
        news_list = news.get_Stock_news()
        if not news_list:
            print("뉴스를 찾을 수 없습니다.")
        else:
            for news in news_list:
                print(f"제목: {news['title']}")
                print(f"링크: {news['link']}")
                print(f"출처: {news['source']}")
                print(f"날짜: {news['date']}")
                print("\n")


# 관심 종목 뉴스
def stock_news_mylist():
    file_path = 'mycode.json'
    result = readConfigjson(file_path)
    for company, stock_code in result:
        # print(f"회사: {company}, 코드: {stock_code}")
        news = Stocknews(stock_code)
        news_list = news.get_Stock_news()
        if not news_list:
            print("뉴스를 찾을 수 없습니다.")
        else:
            for news in news_list:
                print(f"제목: {news['title']}")
                print(f"링크: {news['link']}")
                print(f"출처: {news['source']}")
                print(f"날짜: {news['date']}")
                print("\n")


if __name__ == '__main__':
    # stock_news()
    # stock_news_all()
    stock_news_mylist()
