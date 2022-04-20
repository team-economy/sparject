from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparject


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/memo', methods=['GET'])
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

    doc = []

    db.news.delete_many({})

    for span_tag in soup.findAll('span'):
        span_tag.replace_with('')

    for ar in articles:
        a_tag = ar.select_one('dl > dd.articleSubject > a')
        if a_tag is not None:
            title = ar.select_one('dl > dd.articleSubject > a').text
            summury = ar.select_one('dl > dd.articleSummary').text.strip()
            img = ar.select_one('dl > dt > a > img')['src']
            url = 'https://finance.naver.com/' + ar.select_one('dl > dd.articleSubject > a')['href']

            doc = {'title': title, 'summury': summury, 'img': img, 'url': url}

            db.news.insert_one(doc)

    return jsonify({'msg':'뉴스 최신화'})




if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)


