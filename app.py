from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparject


######## SAVE BUTTON ########
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/stockReload', methods=['POST'])
def stockReload():
    db.stockapi.delete_many({})

    # NEED TO BRING DATA FROM SEARCH RESULT !!  search_results = [] !!

    r = requests.get('https://m.stock.naver.com/api/json/sise/enrollItemListJson.nhn?pageSize=200')

    stockapi = r.json().get('result').get('itemList')

    db.stockapi.delete_many({})

    for i in range(len(stockapi)):
        stock_date = stockapi[i]['thistime'][4:12]
        stock_name = stockapi[i]['nm']
        stock_price = stockapi[i]['pcv']
        stock_pchange = stockapi[i]['cv']
        stock_rate = stockapi[i]['cr']

        doc = {
            'No.': i,
            'Date': stock_date,
            'Name': stock_name,
            'Price': stock_price,
            'Change': stock_pchange,
            'Range': stock_rate

        }
        db.stockapi.insert_one(doc)

    return jsonify({'msg':'뉴스 최신화'})

@app.route('/save', methods=['GET'])
def savestocks():
    stocks = list(db.stockapi.find({'Name':'NAVER'}, {'_id': False}).sort(-1))
    return jsonify({'result': 'success', 'stocks': stocks})

@app.route('/datasave', methods=['POST'])
def poststocks():
    mystocks = list(db.stockapi.find({'Name':'NAVER'}, {'_id': False}))
    return jsonify({'result': 'success', 'mystocks': mystocks})


######### DELETE BUTTON #########
@app.route('/datadlt', methods=['GET'])
def deletedata():
    db.stockapi.delete_one({})
    # return jsonify({'msg':'Deleted!'})

@app.route('/delete', methods=['POST'])
def btndeletedata():
    stocks = list(db.stockapi.find_many({}, {'_id': False}))
    return jsonify({'result': 'success', 'stocks': stocks})

@app.route('/news', methods=['GET'])
def listing():
    articles = list(db.news.find({}, {'_id': False}))
    return jsonify({'all_articles':articles})

@app.route('/news', methods=['POST'])
def show_news():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://finance.naver.com/news/mainnews.naver', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    articles = soup.select("#contentarea_left > div.mainNewsList > ul > li")

    db.news.delete_many({})

    for span_tag in soup.findAll('span'):
        span_tag.replace_with('')

    for ar in articles:
        a_tag = ar.select_one('dl > dd.articleSubject > a')
        if a_tag is not None:
            title = ar.select_one('dl > dd.articleSubject > a').text
            summury = ar.select_one('dl > dd.articleSummary').text.strip()
            url = 'https://finance.naver.com/' + ar.select_one('dl > dd.articleSubject > a')['href']

            news_url = requests.get(url, headers=headers)
            soup_article = BeautifulSoup(news_url.text, 'html.parser')
            img = soup_article.select_one('meta[property="og:image"]')['content']

            doc = {'title': title, 'summury': summury, 'img': img, 'url': url}

            db.news.insert_one(doc)

    return jsonify({'msg':'뉴스 최신화'})




if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)


