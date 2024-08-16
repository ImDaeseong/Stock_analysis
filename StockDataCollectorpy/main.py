from StockCodeDownload import StockCodeDownload
from StockCodeSearch import StockCodeSearch
from StockDataCollection import StockDataCollection


def downlaodCode():
    StockCodeDownload().saveToJson()
    """
    json_data = StockCodeDownload().download_code()
    if json_data:
        print(json_data)
    else:
        print("데이터를 가져오는 데 실패했습니다.")
    """


def searchCode():
    search_key = input("검색어를 입력하세요 (2글자 이상): ")
    results = StockCodeSearch().search(search_key=search_key)

    if isinstance(results, list):
        for item in results:
            print(f"회사명: {item['company']}, 종목코드: {item['code']}")
        return results
    else:
        print(results)
        return []


def searchResult():
    results = searchCode()
    if results:
        try:
            index = int(input("수집할 주식 번호를 입력하세요 (1, 2, ...): ").strip()) - 1
            if 0 <= index < len(results):
                print(results[index]['company'])
                stock_code = results[index]['code']
                CollectData(stock_code)
            else:
                print("유효하지 않은 번호입니다.")
        except ValueError:
            print("잘못된 입력입니다.")


def CollectData(stock_code):

    """
    pages = StockDataCollection(stock_code).getTotalpages()
    print(pages)

    results = StockDataCollection(stock_code).getSelectpages(page=1)
    print(results)
    """

    resultsAll = StockDataCollection(stock_code).getAllPages()
    for item in resultsAll:
        print(item)


def callIndex():
    while True:
        print("\n기능 선택:")
        print("1: 주식 코드 목록")
        print("2: 데이터 수집")
        print("0: 종료")

        select = input("번호를 입력하세요 (1, 2, 0): ").strip()

        if select == '1':
            downlaodCode()
        elif select == '2':
            searchResult()
        elif select == '0':
            print("프로그램을 종료합니다.")
            break
        else:
            print("유효하지 않은 선택입니다.")


if __name__ == '__main__':
    callIndex()
