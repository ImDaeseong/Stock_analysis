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

    stock_instance = StockDataCollection(stock_code)
    json_saver = JSONSaver()

    while True:
        stock_data = stock_instance.get_Stock_info()

        if stock_data:
            print(stock_data)
            json_saver.save(stock_data)

        time.sleep(10)
