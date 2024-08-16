import pandas as pd
import requests
from io import StringIO


class StockCodeDownload:

    url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download'

    def __init__(self, url=None):
        # URL 초기화, 인자가 없으면 기본 URL 사용
        self.url = url or StockCodeDownload.url

    def download_code(self):
        try:
            # URL에서 HTML 데이터 가져옴
            response = requests.get(self.url)
            response.encoding = response.apparent_encoding  # 인코딩 문제 처리
            # print(response.text)

            # StringIO 객체 생성
            html_content = StringIO(response.text)

            # HTML table 데이터를 DataFrame으로 변환
            stock_code = pd.read_html(html_content, header=0)[0]

            # DataFrame에 '회사명','종목코드' 존재 확인
            if '회사명' not in stock_code.columns or '종목코드' not in stock_code.columns:
                raise ValueError("DataFrame에 없습니다.")

            # 필요한 컬럼만 선택
            stock_code = stock_code[['회사명', '종목코드']]

            # 컬럼 이름 변경
            stock_code = stock_code.rename(columns={'회사명': 'company', '종목코드': 'code'})

            # 종목 코드를 6자리로 포맷팅
            stock_code['code'] = stock_code['code'].astype(str).str.zfill(6)

            # DataFrame -> JSON 변환
            json_data = stock_code.to_json(orient='records', lines=True, force_ascii=False)
            return json_data

        except Exception as e:
            print(f"오류 발생: {e}")
            return None

    def saveToJson(self, filename='code.json'):
        json_data = self.download_code()

        if json_data:
            # JSON 데이터를 파일로 저장
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(json_data)
            print(f"종목 코드 '{filename}'에 저장되었습니다.")
        else:
            print("저장할 데이터가 없습니다.")
