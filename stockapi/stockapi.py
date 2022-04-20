import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

r = requests.get('https://m.stock.naver.com/api/json/sise/enrollItemListJson.nhn?pageSize=100')

stockapi = r.json().get('result').get('itemList')

for i in range(len(stockapi)):
    stock_date = stockapi[i]['thistime'][0:8]
    stock_name = stockapi[i]['nm']
    stock_price = stockapi[i]['cv']
    stock_rate = stockapi[i]['cr']

    print(stock_date, stock_name, stock_price, stock_rate)

    doc = {
        'Date': stock_date,
        'Name': stock_name,
        'Price': stock_price,
        'Range': stock_rate

    }
    db.stockapi.insert_one(doc)

    print(doc)