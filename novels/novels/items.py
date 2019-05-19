# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


class YunqiItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class YunqiBookListItem(scrapy.Item):
    novel_id = scrapy.Field()
    novel_name = scrapy.Field()
    novel_link = scrapy.Field()
    novel_author = scrapy.Field()
    novel_type = scrapy.Field(
        input_processor = MapCompose(lambda x: x.replace('[', '').replace(']', ''))
    )
    novel_status = scrapy.Field()
    novel_update_time = scrapy.Field(
        input_processor = MapCompose(lambda x: '20' + x)
    )
    novel_words = scrapy.Field(
        input_processor = MapCompose(lambda x: int(x))
    )
    novel_image_url = scrapy.Field()


class YunqiBookDetailItem(scrapy.Item):
    novel_id = scrapy.Field()
    novel_label = scrapy.Field(
        input_processor=MapCompose(lambda x: x.split('：')[1].strip())
    )
    novel_all_click = scrapy.Field(
        input_processor = MapCompose(lambda x: int(x.split('：')[1]))
    )
    novel_month_click = scrapy.Field(
        input_processor=MapCompose(lambda x: int(x.split('：')[1]))
    )
    novel_week_click = scrapy.Field(
        input_processor=MapCompose(lambda x: int(x.split('：')[1]))
    )
    novel_all_popular = scrapy.Field(
        input_processor=MapCompose(lambda x: int(x.split('：')[1]))
    )
    novel_month_popular = scrapy.Field(
        input_processor=MapCompose(lambda x: int(x.split('：')[1]))
    )
    novel_week_popular = scrapy.Field(
        input_processor=MapCompose(lambda x: int(x.split('：')[1]))
    )
    novel_all_comm = scrapy.Field(
        input_processor=MapCompose(lambda x: int(x.split('：')[1]))
    )
    novel_month_comm = scrapy.Field(
        input_processor=MapCompose(lambda x: int(x.split('：')[1]))
    )
    novel_week_comm = scrapy.Field(
        input_processor=MapCompose(lambda x: int(x.split('：')[1]))
    )
    novel_comment_num = scrapy.Field()