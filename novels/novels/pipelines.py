# -*- coding: utf-8 -*-
import pymongo
from novels.items import *


class YunQicrawlPipeline(object):
    def __init__(self, mongo_uri, mongo_db, replicaset):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.replicaset = replicaset

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'yunqi'),
            replicaset=crawler.settings.get('REPLICASET')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri, replicaset=self.replicaset)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, YunqiBookListItem):
            if self.db.book_info.count_documents({'novel_id': item.get('novel_id')}) == 0:
                self.db.book_info.insert(dict(item))
        else:
            self.db.book_detail.insert(dict(item))
        return item