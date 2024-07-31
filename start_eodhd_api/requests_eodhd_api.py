import requests
import json
from datetime import datetime, timedelta
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

# EODHD API 키
API_KEY = config["EODHD"]["API"]

# API URL
BASE_URL = 'https://eodhistoricaldata.com/api/eod'

# 주식 목록 (국내 및 해외 주식 종목 코드를 포함)
stocks = [
    {'symbol': 'AAPL.US', 'exchange': 'US'},
    {'symbol': '005930.KO', 'exchange': 'KSE'},  # 삼성전자
    # 다른 종목들을 여기에 추가
]

# 날짜 설정 (전날)
yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

# 주식 데이터 가져오기
stock_data = {}

for stock in stocks:
    symbol = stock['symbol']
    url = f"{BASE_URL}/{symbol}?api_token={API_KEY}&fmt=json&date={yesterday}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            stock_data[symbol] = data[0]  # 가장 최근 데이터를 사용
        else:
            print(f"No data found for {symbol}")
    else:
        print(f"Failed to fetch data for {symbol}: {response.status_code}")

# JSON 파일로 저장
with open('requests_eodhd_api_stock_data.json', 'w') as json_file:
    json.dump(stock_data, json_file, indent=4)

print("Data saved to stock_data.json")
