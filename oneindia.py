# -*- coding: utf-8 -*-
import scrapy
import hashlib
from scrapy.linkextractors import LinkExtractor

class OneindiaSpider(scrapy.Spider):
    name = 'oneindia'
    allowed_domains = ['tamil.oneindia.com/news/tamilnadu/']
    start_urls = ['https://tamil.oneindia.com/news/tamilnadu/','https://tamil.oneindia.com/news/india/',
				  'https://tamil.oneindia.com/news/business/'
				  ]
    
    def parse(self,response):
        lnkex = LinkExtractor(unique=True,strip=True)
        links = lnkex.extract_links(response)
        for link in links:
            yield scrapy.http.Request(link.url,callback=self.extract_info)
        
    
    def extract_info(self,response):
        #reponse.follow(link,callback=self.extract_info)
        Title = response.css('h1::text').extract()
        Date = response.css('time::text').extract()[0].strip()
        Article = response.css('.oi-article-lt').xpath('.//p//text()').extract()

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
        

    
