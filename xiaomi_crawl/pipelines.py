# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



# encoding=utf-8
import pymongo
from items import XiaomiCrawlItem


class MongoDBPipleline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["Xiaomiapp"]
        self.XiaomiApp = db["XiaomiApp"]


    def process_item(self, item, spider):
        """ write the crawl item to mongodb """
        if isinstance(item, XiaomiCrawlItem):

            self.XiaomiApp.insert(dict(item))


