from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

@app.route('/')
def home():
   return render_template('index.html')

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://finance.naver.com/news/mainnews.naver',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

#contentarea_left > div.mainNewsList > ul > li:nth-child(1)
#contentarea_left > div.mainNewsList > ul > li:nth-child(2)

articles = soup.select("#contentarea_left > div.mainNewsList > ul > li")

#contentarea_left > div.mainNewsList > ul > li:nth-child(1) > dl > dt > a
#contentarea_left > div.mainNewsList > ul > li:nth-child(2) > dl > dd.articleSubject > a
#contentarea_left > div.mainNewsList > ul > li:nth-child(2) > dl > dd.articleSummary
#contentarea_left > div.mainNewsList > ul > li:nth-child(2) > dl > dt > a > img

for span_tag in soup.findAll('span'):
    span_tag.replace_with('')

for ar in articles:
    a_tag = ar.select_one('dl > dd.articleSubject > a')
    if a_tag is not None:
        title = ar.select_one('dl > dd.articleSubject > a').text
        summury = ar.select_one('dl > dd.articleSummary').text.strip()
        img = ar.select_one('dl > dt > a > img')
        url = ar.select_one('dl > dd.articleSubject > a')

        print(title)
        print(summury)
        print(img['src'])
        print('https://finance.naver.com/'+url['href'])
