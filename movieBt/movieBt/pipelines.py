# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.exceptions import DropItem
from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017/")
database = client["movie"]
collection = database["bt"]


def get_urls():
    '''
    将数据库中已经存在的url作为一个list返回
    '''
    query = {}
    projection = {}
    projection["url"] = u"$url"

    cursor = collection.find(query, projection = projection)

    urls=[]
    try:
        for doc in cursor:
            urls.append(doc['url'])
    finally:
        client.close()

    return urls



class DuplicatesPipeline(object):

    def __init__(self):
        self.urls_seen = get_urls()

    def process_item(self, item, spider):
        if item['url'] in self.urls_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            return item


class MoviebtPipeline(object):
    '''
    将数据写入mongoDB中
    '''
    
    collection_name = 'bt'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri='127.0.0.1',
            mongo_db='movie'
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item