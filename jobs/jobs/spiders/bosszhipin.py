# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider


class BosszhipinSpider(CrawlSpider):
    name = 'bosszhipin'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/']
    # redis_key = 'bosszhipin:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r'.*/job_detail/.+\.html$'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
