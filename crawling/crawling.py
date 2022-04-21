import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://finance.naver.com/marketindex/exchangeList.naver', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
trs = soup.select(
    '#_cs_foreigninfo > div > div.api_cs_wrap > div > div.c_rate > div.rate_table_bx._table > table > tbody > tr')


def return_value(address, addition):
    res = requests.get(address + addition)
    soup = BeautifulSoup(res.content, 'html.parser')

    frame = soup.find('iframe', id="frame_ex1")
    frameaddr = address + frame['src']

    res1 = requests.get(frameaddr)
    frame_soup = BeautifulSoup(res1.content, 'html.parser')
    items = frame_soup.select('body > div > table > tbody > tr')

    for item in items:
        name = item.select('td')[0].text.replace("\n", "")
        name = name.replace("\t", "")
        print(name + "\t" + item.select('td')[1].text)


baseaddress = 'https://finance.naver.com'
info = '/marketindex/?tabSel=exchange#tab_section'
return_value(baseaddress, info)
