from flask import Flask, render_template, jsonify
app = Flask(__name__)
import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparject
stockdb = db.stockapi

#NEED TO BRING DATA FROM SEARCH RESULT !!  search_results = [] !!

r = requests.get('https://m.stock.naver.com/api/json/sise/enrollItemListJson.nhn?pageSize=200')

stockapi = r.json().get('result').get('itemList')

for i in range(len(stockapi)):
    stock_date = stockapi[i]['thistime'][0:8]
    stock_name = stockapi[i]['nm']
    stock_price = stockapi[i]['pcv']
    stock_pchange = stockapi[i]['cv']
    stock_rate = stockapi[i]['cr']

    print(stock_date, stock_name, stock_price, stock_rate)

    doc = {
        'No.': i,
        'Date': stock_date,
        'Name': stock_name,
        'Price': stock_price,
        'Change': stock_pchange,
        'Range': stock_rate

    }
    db.stockapi.sort(-1)
    db.stockapi.insert_one(doc)

    print(doc)

# SAVE BUTTON #
# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/stockdata', method=['GET'])
# def savedata():
#     stockapi = list(db.stockapi.find({}, {'_id': False}))
#     return stockapi.find_one()
#

######## DELETE BUTTON #########

@app.route('/dltdb', methods=['POST'])
def deletedb():
    db.stockapi.delete_one({})
    return jsonify({'msg':'Deleted!'})

@app.route('/dltdata', method=['GET'])
def showdata():
    mylist = list(db.stockapi.find({}, {'_id': False}))
    return mylist.find_one()


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)