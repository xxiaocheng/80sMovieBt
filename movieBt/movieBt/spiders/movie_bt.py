# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import MoviebtItem

class MovieBtSpider(scrapy.Spider):
    name = 'movie_bt'

    def start_requests(self):
        urls=['https://www.80s.tw/movie/list']

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse_urls)
    
    def parse_urls(self,response):
        
        for url in response.css('div#block3 li  h3 a::attr(href)').extract():
            yield response.follow(url,self.parse)
        
        next_page=response.xpath('//*[@id="block3"]/div[3]/div/a/@href').extract()
        if len(next_page)!=0:
            yield response.follow(next_page[-2],self.parse_urls)

    def parse(self, response):
        item=MoviebtItem()

        title=response.xpath('//title//text()').extract_first()[1:]
        item['name']=title.split(' ')[0]
        item['year']=re.findall(r'\((.*?)\)',title)[0]
        item['url']=response.url
        item['score']=response.xpath('//*[@id="minfo"]/div[2]/div[2]/span[1]/text()').extract()[2].strip()
        item['tags']=response.xpath('//*[@id="minfo"]/div[2]/div[1]/span[1]/a/text()').extract()
        item['comments']=response.xpath('//*[@id="minfo"]/div[2]/div[2]/span[2]/a/@href').extract_first()
        item['bts']=response.xpath('//*[@id="myform"]/ul/li/span[2]/a/@href').extract()

        return item