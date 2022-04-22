from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:메일주소.tbpbs.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

# from pymongo import MongoClient
# client = MongoClient('localhost', 27017)
# db = client.dbsparta

import requests
from bs4 import BeautifulSoup


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/stockapi/search', methods=['POST'])
def search():
    stock_receive = request.args.get('stockname')
    searchlist = list(db.stockapi.({'Name': 'name'}))
    return jsonify({'msg':'포스트 완료'})

@app.route('/stockapi', methods=['GET'])
def search():
    searchresult = request.args.get('stockname')
    getlist = list(db.stockapi.find({'Name': 'stockname'}))
    return jsonify({'stockname_data':getlist})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

# for getstock in getlist:
#     print(getstock['Name'])
