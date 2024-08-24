import json
from StockAnalyzer1 import StockAnalyzer1
from StockAnalyzer2 import StockAnalyzer2
from StockAnalyzer3 import StockAnalyzer3
from StockAnalyzer4 import StockAnalyzer4
from StockDataCollection import StockDataCollection
from StockDatabase import StockDatabase


def load_code(filename='code.json'):
    try:
        records = []
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                record = json.loads(line)
                records.append(record)
        return records
    except Exception as e:
        print(f"오류 발생: {e}")
        return None


def read_config(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get('stock_code')
    except Exception as e:
        print(f"오류 발생: {e}")
        return None


def save_file(file_name, results):
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(results)
    except Exception as e:
        print(f"파일 저장 오류 발생: {e}")


def CollectDataDB(stock_code):
    db = StockDatabase()

    # 기존 데이터 삭제
    db.delete_data(stock_code)

    resultsAll = StockDataCollection(stock_code).getAllPages()
    db.insert_data(stock_code, resultsAll)
    db.close()

    print(f"총 {len(resultsAll)}개 데이터 저장")


# 이동 평균선
def get_A1(stock_code):
    """
    Buy_Signal 1 이면 매수, Sell_Signal 0, -1 매도, Position 1 이면 변경 감지
    """
    analyzer = StockAnalyzer1()
    result_df = analyzer.analyze_Data(stock_code)
    print(result_df)
    return "==== 이동 평균선 분석  ====\n" + result_df.to_string()


def get_A2(stock_code):
    """
    14일 기간동안  70 이상이면 과매수, 30 이하이면 과매도
    """
    analyzer = StockAnalyzer2()
    result_df = analyzer.analyze_Data(stock_code)
    print(result_df)
    return "==== 14일 기간동안  70 이상이면 과매수, 30 이하이면 과매도 분석 ====\n" + result_df.to_string()


def get_A3(stock_code):
    """
    가격이 상한 밴드 가격보다 높으면 과매수, 하한 밴드이하이면 과매도
    """
    analyzer = StockAnalyzer3()
    result_df = analyzer.analyze_Data(stock_code)
    print(result_df)
    return "==== 가격이 상한 밴드 가격보다 높으면 과매수, 하한 밴드이하이면 과매도 분석 ====\n" + result_df.to_string()


def get_A4(stock_code):
    """
    %K가 %D 위로 돌파하면 매수 신호, 아래로 돌파하면 매도 신호
    """
    analyzer = StockAnalyzer4()
    result_df = analyzer.analyze_Data(stock_code)
    print(result_df)
    return "==== K가 %D 위로 돌파하면 매수 신호, 아래로 돌파하면 매도 신호 분석 ====\n" + result_df.to_string()


if __name__ == '__main__':

    data_list = load_code('code.json')
    if data_list is not None:
        for idx, record in enumerate(data_list):
            # print(f"Index {idx}: {record}")

            stock_company = record.get('company')
            stock_code = record.get('code')
            # print(f"{stock_company}: {stock_code}")

            if stock_code:
                CollectDataDB(stock_code)

                # 모든 분석 결과
                all_results = (
                        get_A1(stock_code) + "\n\n" +
                        get_A2(stock_code) + "\n\n" +
                        get_A3(stock_code) + "\n\n" +
                        get_A4(stock_code)
                )

                file_name = f"{stock_company}_{stock_code}.txt"
                save_file(file_name, all_results)
                print(f"결과가 {file_name}에 저장되었습니다.")
            else:
                print(f"오류 발생: {file_name}")
    else:
        print("데이터 로드 실패했습니다.")

