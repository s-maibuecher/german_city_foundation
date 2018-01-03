# -*- coding: utf-8 -*-
import scrapy


class MyWikiSpiderSpider(scrapy.Spider):
    name = "my-wiki-spider"
    allowed_domains = ["https://de.wikipedia.org/wiki/Liste_deutscher_Stadtgr%C3%BCndungen"]
    start_urls = ['http://https://de.wikipedia.org/wiki/Liste_deutscher_Stadtgr%C3%BCndungen/']

    def parse(self, response):
        pass
