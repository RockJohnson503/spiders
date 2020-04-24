# encoding: utf-8

"""
File: run.py
Author: Rock Johnson
"""
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

process.crawl('yunqi')
process.start()