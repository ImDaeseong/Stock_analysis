import json
import time

from StockDataCollection import StockDataCollection, JSONSaver


def readConfig(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data.get('stock_code')


if __name__ == '__main__':

    # print("현재 경로:", os.getcwd())

    config_path = 'config.json'
    stock_code = readConfig(config_path)

    if not stock_code:
        print("json 파일 읽기 실패")
        exit(1)

    stock_data = StockDataCollection(stock_code)
    json_saver = JSONSaver()

    while True:
        price_info = stock_data.get_current_price_info()

        if price_info:
            print(price_info)
            json_saver.save(price_info)

        time.sleep(10)
