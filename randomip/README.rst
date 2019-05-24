=====
Randomip
=====

randomip是一个随机ip代理池,可以很好的在scrapy中使用,且无需维护ip池.

Quick start
-----------

1. 安装randomip.

::

    cd randomip

    pip install dist/randomip-1.0.tar.gz

2. 使用randomip.

.. code-block:: python

    >>> from randomip.randomip import XiciIp

    >>> ip = XiciIp(page_size=2)

    >>> ip.get_random_ip()
    'https://112.85.128.209:9999'

3. 在scrapy中使用randomip.

.. code-block:: python
    from randomip import randomip


    class SpiderMiddleware:
        def __init__(self, crawler):
            cs = crawler.signals
            cs.connect(self.spider_opened, signal=signals.spider_opened)

        @classmethod
        def from_crawler(cls, crawler):
            return cls(crawler)

        def spider_opened(self, spider):
            self.ips = randomip.KuaiIp(spider=spider, delay=self.delay, page_size=self.page_size, concurrent=self.concurrent, headers=self.headers)

        def process_request(self, request, spider):
            request.meta['proxy'] = self.ips.get_random_ip()

4. 在scrapy中实例化时,spider为必填属性,后面的属性可以根据自己的需求来填.