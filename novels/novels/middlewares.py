# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from randomip import randomip
from twisted.internet.error import TimeoutError, ConnectError
from scrapy import signals
import random, requests


class NovelsSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class NovelsDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware:
    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        agents = crawler.settings.getlist('USER_AGENTS')
        return cls(agents)

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))


class RandomIpProxyMiddleware:
    def __init__(self, agents, delay, page_size, concurrent, crawler):
        self.agents = agents
        self.delay = delay
        self.page_size = page_size
        self.concurrent = concurrent
        cs = crawler.signals
        cs.connect(self.spider_opened, signal=signals.spider_opened)

    @classmethod
    def from_crawler(cls, crawler):
        agents = crawler.settings.getlist('USER_AGENTS')
        delay = crawler.settings.get('DOWNLOAD_DELAY')
        page_size = crawler.settings.get('GET_IP_PAGE_SIZE')
        concurrent = crawler.settings.get('CONCURRENT_RANDOMIP')
        return cls(agents, delay, page_size, concurrent, crawler)

    def spider_opened(self, spider):
        # headers = {'User-Agent': random.choice(self.agents)}
        # self.ips = randomip.KuaiIp(spider=spider, delay=self.delay, page_size=self.page_size, concurrent=self.concurrent, headers=headers)
        self._url = 'http://tpv.daxiangdaili.com/ip/?tid=559058343128731&num=1&protocol=http'
        self.proxy = 'http://%s' % requests.get(self._url).text

    def process_request(self, request, spider):
        # request.meta['proxy'] = self.ips.get_random_ip('https')
        print('正在下载', self.proxy, request.url)
        request.meta['proxy'] = self.proxy

    def process_response(self, request, response, spider):
        print('下载成功:', response.status, request.meta['proxy'])
        return response

    def process_exception(self, request, exception, spider):
        print('下载失败:', request.meta['proxy'], type(exception), request.url)
        if isinstance(exception, (TimeoutError, ConnectError)):
            if request.meta['proxy'] == self.proxy:
                self.proxy = 'http://%s' % requests.get(self._url).text
                print('切换成功:', self.proxy)
            request.priority = 1
            return request