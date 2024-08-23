from StockCodeDownload import StockCodeDownload
from StockCodeSearch import StockCodeSearch
from StockDataCollection import StockDataCollection
from StockDatabase import StockDatabase

# 전역 변수
selected_stock_code = None


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
        global selected_stock_code
        for idx, item in enumerate(results, start=1):
            print(f"{idx}. 회사명: {item['company']}, 종목코드: {item['code']}")
        return results
    else:
        print(results)
        return []


def searchResult():
    global selected_stock_code
    results = searchCode()
    if results:
        try:
            index = int(input("수집할 주식 번호를 입력하세요 (1, 2, ...): ").strip()) - 1
            if 0 <= index < len(results):
                print(results[index]['company'])
                selected_stock_code = results[index]['code']
                CollectData(selected_stock_code)
            else:
                print("유효하지 않은 번호입니다.")
        except ValueError:
            print("잘못된 입력입니다.")


def searchResultDB():
    global selected_stock_code
    results = searchCode()
    if results:
        try:
            index = int(input("수집할 주식 번호를 입력하세요 (1, 2, ...): ").strip()) - 1
            if 0 <= index < len(results):
                print(results[index]['company'])
                selected_stock_code = results[index]['code']
                CollectDataDB(selected_stock_code)
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


def CollectDataDB(stock_code):
    resultsAll = StockDataCollection(stock_code).getAllPages()
    """
    for item in resultsAll:
        print(item)
    """

    db = StockDatabase()
    db.insert_data(stock_code, resultsAll)
    db.close()

    print(f"총 {len(resultsAll)}개 데이터 저장")


def Select_CollectDataDB():
    global selected_stock_code
    if selected_stock_code:
        db = StockDatabase()

        count = db.count_data(selected_stock_code)
        print(f"'{selected_stock_code}'에 대한 총 데이터 개수: {count}")

        if count > 0:
            data = db.select_data(selected_stock_code)
            db.close()

            for row in data:
                print(
                    f"ID: {row[0]}, 코드: {row[1]}, 날짜: {row[2]}, 종가: {row[3]}, 전일비: {row[4]}, 시가: {row[5]}, 고가: {row[6]}, 저가: {row[7]}, 거래량: {row[8]}")
        else:
            print("해당 코드에 대한 데이터가 없습니다.")
            db.close()
    else:
        print("먼저 '2' 또는 '3'을 선택하여 주식 코드를 선택하세요.")


def callIndex():
    while True:
        print("\n기능 선택:")
        print("1: 주식 코드 목록")
        print("2: 데이터 수집")
        print("3: 데이터DB 수집")
        print("4: DB 데이터 조회")
        print("0: 종료")

        try:
            select = input("번호를 입력하세요 (1, 2, 3, 4, 0): ").strip()

            if select == '1':
                downlaodCode()
            elif select == '2':
                searchResult()
            elif select == '3':
                searchResultDB()
            elif select == '4':
                Select_CollectDataDB()
            elif select == '0':
                print("프로그램을 종료합니다.")
                break
            else:
                print("유효하지 않은 선택입니다.")
        except KeyboardInterrupt:
            print("\n프로그램이 사용자에 의해 종료되었습니다.")
            break
        except Exception as e:
            print(f"오류가 발생했습니다: {e}")


if __name__ == '__main__':
    callIndex()
