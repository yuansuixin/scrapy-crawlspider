# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from dushu.items import DushuItem

class DuSpider(CrawlSpider):
    name = 'du'
    allowed_domains = ['www.dushu.com']
    start_urls = ['https://www.dushu.com/book/1181_1.html']
    # 规则是一个元组，可以写多个规则，每一个对着就是Rule对象，
    # 参数1：LinkExtractor(allow=r'Items/')链接提取器
    # 参数2：回调，处理链接提取器提取的url的响应结果，
    # callback=方法名，和Spider不同
    # 参数3：跟进，是否要接着按照这个规则进行提取链接
    page_link = LinkExtractor(allow=r'/book/1181_\d+\.html$')
    rules = (
        Rule(page_link, callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        book_li_list = response.xpath('//div[@class="bookslist"]/ul/li')
        for book in book_li_list:
            item = DushuItem()
            item['book_image_url'] = book.xpath('.//div[@class="book-info"]/div/a/img/@data-original').extract_first()
            item['book_name'] = book.xpath('.//div[@class="book-info"]/div/a/img/@alt').extract_first()
            item['book_author'] = book.xpath('.//div[@class="book-info"]/p/a/text()').extract_first()
            # 接着发送请求，去详情页获取其他信息
            book_url ="http://www.dushu.com"+ book.xpath('.//div[@class="book-info"]/h3/a/@href').extract_first()
            print(item['book_name'])
            print(item['book_image_url'])
            # yield item
            yield scrapy.Request(url=book_url,callback=self.parse_info,meta={'item':item})


    def parse_info(self,response):
        item = response.meta['item']
        #获取其他信息
        item['book_price'] = response.xpath('//div[@class="book-details"]//span/text()').extract_first()
        #简介
        item['book_info'] = response.xpath('//div[@class="book-summary"]/div/div/text()').extract_first()
        item['book_publish'] = response.xpath('//div[@class="book-summary"]/div/div/text()').extract_first()
        yield item
















