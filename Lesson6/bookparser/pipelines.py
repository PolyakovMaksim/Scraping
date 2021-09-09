# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class BookparserPipeline:

    def __init__(self):
        client = MongoClient('Localhost', 27017)
        self.mongo_base = client.book


    def process_item(self, item, spider):
        item['basic_price'], item['discount_price'], item['rating'] = self.process_price(item['basic_price'], item['discount_price'], item['rating'])
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_price(self, basic_price, discount_price, rating):
        basic_price = float(basic_price)
        discount_price = float(discount_price)
        rating = float(rating)
        return basic_price, discount_price, rating

