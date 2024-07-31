import json
from datetime import datetime, timedelta
from eodhd import APIClient
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

# EODHD API 키
API_KEY = config["EODHD"]["API"]

# API 클라이언트 인스턴스 생성
api = APIClient(API_KEY)

# 주식 목록 (국내 및 해외 주식 종목 코드를 포함)
stocks = [
    {'symbol': 'AAPL.US'},  # 애플
    {'symbol': '005930.KO'}  # 삼성전자
    # 다른 종목들을 여기에 추가
]

# 날짜 설정 (전날)
yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

# 주식 데이터 가져오기
stock_data = {}

for stock in stocks:
    symbol = stock['symbol']
    data = api.get_eod_historical_stock_market_data(
        symbol=symbol, 
        period='d', 
        from_date=yesterday, 
        to_date=yesterday, 
        order='a'
    )
    
    if data:
        stock_data[symbol] = data
    else:
        print(f"No data found for {symbol}")

# JSON 파일로 저장
with open('lib_eodhd_stock_data.json', 'w') as json_file:
    json.dump(stock_data, json_file, indent=4)

print("Data saved to stock_data.json")
