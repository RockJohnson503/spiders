# encoding: utf-8

"""
File: dupefilters.py
Author: Rock Johnson
"""
from scrapy.dupefilters import RFPDupeFilter
from w3lib.url import canonicalize_url
from pybloom.pybloom import ScalableBloomFilter
import hashlib


class URLBloomFilter(RFPDupeFilter):
    def __init__(self, path=None, debug=False):
        self.urls_sbf = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)
        RFPDupeFilter.__init__(self, path, debug)

    def request_seen(self, request):
        fp = hashlib.sha1()
        fp.update(canonicalize_url(request.url).encode())
        url_sha1 = fp.hexdigest()
        if url_sha1 in self.urls_sbf:
            return True
        self.urls_sbf.add(url_sha1)