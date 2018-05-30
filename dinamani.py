# -*- coding: utf-8 -*-
import scrapy
import hashlib
from scrapy.linkextractors import LinkExtractor


class DinamaniSpider(scrapy.Spider):
    name = 'dinamani'
    allowed_domains = ['dinamani.com']
    start_urls = ['http://http://www.dinamani.com/india/','http://www.dinamani.com/world/',
				  'http://www.dinamani.com/business/','http://www.dinamani.com/sports/',
				  'http://www.dinamani.com/tamilnadu/',
				]

    def parse(self,response):
        lnkex = LinkExtractor(unique=True,strip=True)
        links = lnkex.extract_links(response)
        for link in links:
            yield scrapy.http.Request(link.url,callback=self.extract_info)
        
    
    def extract_info(self,response):
        #reponse.follow(link,callback=self.extract_info)
        Title =   response.css('h1::text').extract()
        Date = response.css('.ArticlePublish').xpath('./span/text()').extract()[1].strip()
        Article = response.css('.content').xpath('.//p//text()').extract()


        text = ""
        title = ""
        date_time = ""
                
        for para in Article:
            text = text + "\n" +para

        for sent in Title:
            title = title + sent

        for dt in Date:
            date_time = date_time + " " + dt

        if text!="" and date_time!="":
            temp = title.encode()
            m = hashlib.md5(temp)
            scraped_info = {
                    'DOCID' : str(m.hexdigest()),
                    'TITLE' : title,
                    'DATE' : date_time,
                    'ARTICLE' : text
                }
            yield scraped_info
        
