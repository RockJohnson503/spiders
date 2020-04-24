# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from novels.items import *
from urllib import parse
import requests, json


class YunqiSpider(CrawlSpider):
    name = 'yunqi'
    allowed_domains = ['yunqi.qq.com']
    # redis_key = 'yunqi:start_urls'
    start_urls = ['http://yunqi.qq.com/bk']

    rules = (
        Rule(LinkExtractor(allow=r'yunqi.qq.com/bk/.*/.*', deny=(r'yunqi.qq.com/bk/.*\.html$', r'.*book.bookUrl.*')), callback='parse_book_list', follow=True),
    )

    def parse_book_list(self, response):
        item_loader = YunqiItemLoader(item=YunqiBookListItem(), response=response)

        for book in response.css('#detailedBookList .book'):
            item_loader.add_value('novel_image_url', parse.urljoin(response.url, book.css('a img::attr(src)').get()))
            item_loader.add_value('novel_id', book.css('.book_info h3 a::attr(id)').get())
            item_loader.add_value('novel_name', book.css('.book_info h3 > a::text').get())
            item_loader.add_value('novel_link', book.css('.book_info h3 > a::attr(href)').get())
            novel_infos = book.css('.book_info dl dd.w_auth')
            novel_author = ''
            novel_type = ''
            novel_status = ''
            novel_update_time = ''
            novel_words = 0
            if len(novel_infos) > 4:
                novel_author = novel_infos[0].css('a::text').get('')
                novel_type = novel_infos[1].css('a::text').get('')
                novel_status = novel_infos[2].css('::text').get('')
                novel_update_time = novel_infos[3].css('::text').get('')
                novel_words = novel_infos[4].css('::text').get('')

            item_loader.add_value('novel_author', novel_author)
            item_loader.add_value('novel_type', novel_type)
            item_loader.add_value('novel_status', novel_status)
            item_loader.add_value('novel_update_time', novel_update_time)
            item_loader.add_value('novel_words', novel_words)

        book_item = item_loader.load_item()
        # novel_link = book_item.get('novel_link')
        # novel_id = book_item.get('novel_id')
        yield book_item
        # if novel_link:
        #     yield response.follow(novel_link, callback=self.parse_book_detail, meta={'novel_id': novel_id})

    def parse_book_detail(self, response):
        item_loader = YunqiItemLoader(item=YunqiBookDetailItem(), response=response)
        item_loader.add_value('novel_id', response.meta.get('novel_id', ''))
        item_loader.add_css('novel_label', '.tags::text')
        item_loader.add_css('novel_all_click', '#novelInfo tr:nth-child(2) td:nth-child(1)::text')
        item_loader.add_css('novel_month_click', '#novelInfo tr:nth-child(3) td:nth-child(1)::text')
        item_loader.add_css('novel_week_click', '#novelInfo tr:nth-child(4) td:nth-child(1)::text')
        item_loader.add_css('novel_all_popular', '#novelInfo tr:nth-child(2) td:nth-child(2)::text')
        item_loader.add_css('novel_month_popular', '#novelInfo tr:nth-child(3) td:nth-child(2)::text')
        item_loader.add_css('novel_week_popular', '#novelInfo tr:nth-child(4) td:nth-child(2)::text')
        item_loader.add_css('novel_all_comm', '#novelInfo tr:nth-child(2) td:nth-child(3)::text')
        item_loader.add_css('novel_month_comm', '#novelInfo tr:nth-child(3) td:nth-child(3)::text')
        item_loader.add_css('novel_week_comm', '#novelInfo tr:nth-child(4) td:nth-child(3)::text')
        novel_id = response.css('.auther::text').get()
        if novel_id:
            novel_id = novel_id.split('：')[1]
            headers = {'Referer': response.url, 'User-Agent': response.request.headers.get('User-Agent').decode()}
            proxies = {'': ''}
            json_data = requests.get('http://yunqi.qq.com/novelcomment/index.html?bid=%s' % novel_id,
                                       headers=headers, proxies=proxies).text
            data = json.loads(json_data)
            item_loader.add_value('novel_comment_num', data['data']['commentNum'])
            yield item_loader.load_item()