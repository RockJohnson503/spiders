# encoding: utf-8

"""
File: dupefilters.py
Author: Rock Johnson
"""
from scrapy_redis.dupefilter import RFPDupeFilter
from .redisbloom import RedisBloomFilter


class URLBloomFilter(RFPDupeFilter):
    def __init__(self, server, key, debug=False):
        RFPDupeFilter.__init__(self, server, key, debug)
        self.df = RedisBloomFilter(server, key)

    def request_seen(self, request):
        fp = self.request_fingerprint(request)
        if fp in self.df:
            return True
        self.df.add(fp)
        return False