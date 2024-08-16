import json


class StockCodeSearch:

    filename = 'code.json'

    def __init__(self, filename=None):
        self.filename = filename or StockCodeSearch.filename

    def search(self, search_key=None):
        if not search_key or len(search_key) < 2:
            print("검색어는 2글자 이상")
            return

        # 대소문자 구분없이 검색을 위해 검색어를 소문자로 변환
        search_key = search_key.lower()

        try:
            # 파일 읽기
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = [json.loads(line) for line in file]

            # 대소문자 구분없이 검색을 위해 검색어를 소문자로 변환
            results = [entry for entry in data if search_key in entry['company'].lower()]

            # 검색어 포함 필터링
            # results = [entry for entry in data if search_key in entry['company']]

            if results:
                return results
            else:
                return "검색 결과가 없습니다."

        except FileNotFoundError:
            return f"파일 '{self.filename}'을(를) 찾을 수 없습니다."
        except json.JSONDecodeError:
            return "JSON 파일을 읽는 중 오류가 발생했습니다."
        except Exception as e:
            return f"오류 발생: {e}"


