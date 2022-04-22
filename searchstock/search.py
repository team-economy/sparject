from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import requests
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparject

######## SAVE BUTTON ########
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def saving():
    name_receive = request.form['name_give']
    print(name_receive)
    search_result = list(db.stockapi.find({'Name':name_receive},{'_id':False}))
    return jsonify({'result':search_result})

# db.stockapi.delete_many({})
#
# #NEED TO BRING DATA FROM SEARCH RESULT !!  search_results = [] !!
#
# r = requests.get('https://m.stock.naver.com/api/json/sise/enrollItemListJson.nhn?pageSize=200')
#
# stockapi = r.json().get('result').get('itemList')
#
# db.stockapi.delete_many({})
#
# for i in range(len(stockapi)):
#     stock_date = stockapi[i]['thistime'][4:12]
#     stock_name = stockapi[i]['nm']
#     stock_price = stockapi[i]['pcv']
#     stock_pchange = stockapi[i]['cv']
#     stock_rate = stockapi[i]['cr']
#
#     doc = {
#         'No.': i,
#         'Date': stock_date,
#         'Name': stock_name,
#         'Price': stock_price,
#         'Change': stock_pchange,
#         'Range': stock_rate
#
#     }
#     db.stockapi.insert_one(doc)

######## SAVE BUTTON ########
# @app.route('/')
# def home():
#     return render_template('index.html')
#
# @app.route('/save', methods=['GET'])
# def savestocks():
#     stocks = list(db.stockapi.find({'Name':'NAVER'}, {'_id': False}).sort(-1))
#     return jsonify({'result': 'success', 'stocks': stocks})
#
# @app.route('/datasave', methods=['POST'])
# def poststocks():
#     mystocks = list(db.stockapi.find({'Name':'NAVER'}, {'_id': False}))
#     return jsonify({'result': 'success', 'mystocks': mystocks})
#
#
# ######### DELETE BUTTON #########
# @app.route('/datadlt', methods=['GET'])
# def deletedata():
#     db.stockapi.delete_one({})
#     # return jsonify({'msg':'Deleted!'})
#
# @app.route('/delete', methods=['POST'])
# def btndeletedata():
#     stocks = list(db.stockapi.find_many({}, {'_id': False}))
#     return jsonify({'result': 'success', 'stocks': stocks})
#
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

