# -*- coding: utf-8 -*-
import scrapy


class YunqiBookListItem(scrapy.Item):
    novel_id = scrapy.Field()
    novel_name = scrapy.Field()
    novel_link = scrapy.Field()
    novel_author = scrapy.Field()
    novel_type = scrapy.Field()
    novel_status = scrapy.Field()
    novel_update_time = scrapy.Field()
    novel_words = scrapy.Field()
    novel_image_url = scrapy.Field()


class YunqiBookDetailItem(scrapy.Item):
    novel_id = scrapy.Field()
    novel_label = scrapy.Field()
    novel_all_click = scrapy.Field()
    novel_month_click = scrapy.Field()
    novel_week_click = scrapy.Field()
    novel_all_popular = scrapy.Field()
    novel_month_popular = scrapy.Field()
    novel_week_popular = scrapy.Field()
    novel_comment_num = scrapy.Field()
    novel_all_comm = scrapy.Field()
    novel_month_comm = scrapy.Field()
    novel_week_comm = scrapy.Field()