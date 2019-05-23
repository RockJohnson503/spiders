# encoding: utf-8

"""
File: xici_ip.py
Author: Rock Johnson
"""
import requests, random
from treq import request, content
from scrapy.selector import Selector
from twisted.internet import reactor, defer, task


class GetIp:
    def __init__(self, delay=0, page_size=None, concurrent=16, headers=None):
        self.ips = []
        self.delay = delay
        self.page_size = page_size
        self.concurrent = concurrent
        self.headers = headers
        self._crawl_ip()
        reactor.run()

    def _crawl_ip(self):
        # 爬取西刺的ip代理
        page_size = self.page_size
        if not page_size:
            html = requests.get("https://www.xicidaili.com/nn", headers=self.headers)
            page_size = int(Selector(text=html.text).css(".pagination a:nth-child(13)::text").get(""))
        works = (self._treq_crawl_ip(url) for url in range(1, page_size))
        coop = task.Cooperator()
        join = defer.DeferredList([coop.coiterate(works) for i in range(self.concurrent)])
        join.addCallback(lambda _: reactor.stop())

    @defer.inlineCallbacks
    def _treq_crawl_ip(self, url):
        yield task.deferLater(reactor, self.delay, lambda: None)
        re = request('GET', 'https://www.xicidaili.com/nn/%d' % url, headers=self.headers)
        re.addCallback(self._treq_download_page)
        yield re

    @defer.inlineCallbacks
    def _treq_download_page(self, response):
        if response.code >= 200 and response.code < 300:
            con = content(response)
            con.addCallback(self._treq_get_content)
            yield con

    def _treq_get_content(self, content):
        select = Selector(text=content.decode())
        all_trs = select.css("#ip_list tr")

        for tr in all_trs[1:]:
            all_texts = tr.css("td")
            ip = all_texts[1].css('::text').get().strip()
            port = all_texts[2].css('::text').get().strip()
            proxy_type = all_texts[5].css('::text').get().strip()

            ip = '%s://%s:%s' % (proxy_type, ip, port)
            if ip not in self.ips:
                self.ips.append(ip)

    def get_random_ip(self):
        # 随机获取ip代理
        return random.choice(self.ips)

    def judge_ip(self):
        http_url = "https://www.baidu.com"
        errcount = 0

        for ip in self.ips:
            try:
                proxy_dict = {
                    ip[:ip.index('://')]: ip
                }
                res = requests.get(http_url, proxies=proxy_dict, timeout=2)
            except:
                self.delete_ip(ip)
                errcount += 1
            else:
                code = res.status_code
                if code >= 200 and code < 300:
                    continue
                else:
                    self.delete_ip(ip)
                    errcount += 1
        return errcount

    def delete_ip(self, ip):
        # 删除错误的ip
        self.ips.remove(ip)