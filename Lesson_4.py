from lxml import html
import requests
from pymongo import MongoClient
from _datetime import datetime as dt
import hashlib

client = MongoClient('127.0.0.1', 27017)
db = client['News']
lenta = db.news_from_lenta

today = dt.now()

my_headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
response = requests.get('https://lenta.ru/', headers = my_headers)

if response.ok:

    dom = html.fromstring(response.text)

    items = dom.xpath("//div[@class='item']")

    for item in items:
        name = item.xpath('./a/text()')[0].replace("\xa0", ' ')
        link = item.xpath('./a/@href')[0]
        try:
            datetime = item.xpath('.//time/@datetime')[0]
        except:
            datetime = today
        source = 'https://lenta.ru/'

        if link[0] == '/':
            link = (source + link[1:])

        my_dict = {'name': name, 'link': link}

        news_hash = hashlib.sha1()
        news_hash.update(repr(my_dict).encode('utf-8'))
        id = news_hash.hexdigest()


        try:
            lenta.insert_one({'_id': id, 'name' : name, 'link' : link, 'datetime' : datetime, 'source' : source})
        except:
            continue

