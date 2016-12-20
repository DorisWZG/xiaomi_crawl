
# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import scrapy_splash
from scrapy_splash import SplashRequest
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from xiaomi_crawl.items import XiaomiCrawlItem


class XiaomiSpider(scrapy.Spider):
    name = "xiaomi"
    allowed_domains = ["mi.com"]
    start_urls = [
        "http://app.mi.com/category/15"
    ]#"http://app.mi.com/category/15"
    def start_requests(self):
        url=self.start_urls[0]
        args={
            'har': 1,
            'html': 1,
        }

        yield SplashRequest(url,self.parse, endpoint='render.json',args=args)

    def parse(self, response):
        #with beautifulsoup find all game related item
        #with splash script 'go to next page' function is implemented and the corresponding link is returned(javascript site cannot be seen)
        # ...
        script = """
        function main(splash)
        local url = splash.args.url
        assert(splash:go(url))
        assert(splash:wait(0.5))
        assert(splash:autoload("https://code.jquery.com/jquery-2.1.3.min.js"))
        splash:runjs("document.getElementsByClassName('next')[0].click()")
        assert(splash:wait(1))
        local href = splash:evaljs("window.location.href")
         assert(splash:wait(1))
        return {
            html = splash:html(),
            png = splash:png(),
            har = splash:har(),
            href = href,
        }
        end
        """
        # ...
        args={
            'har': 1,
            'html': 1,
            'lua_source':script,
        }

        soup=BeautifulSoup(response.data[u'html'])
        all_app=soup.find("ul",{"id":"all-applist"})
        applist=all_app.find_all("li")
        for app in applist:
            item=XiaomiCrawlItem()
            link=app.a['href']
            item['link']=link
            image=app.a.img['src']
            item['image_link']=image
            text=app.h5.a.contents[0]
            item['text']=text
            category_link=app.p.a['href']
            item['category_link']=category_link
            category=app.p.a.contents[0]
            item['category']=category
            yield item
        if u'href' in response.data:
            url=response.data[u'href']
            #print "yes",url
        else:
            url=response.url
            #print "no",url

        yield SplashRequest(url,self.parse, endpoint='execute',args=args)




