# -*- coding: utf-8 -*-
import scrapy
import hashlib
from scrapy.linkextractors import LinkExtractor


class DailythantiSpider(scrapy.Spider):
    name = 'dailythanti'
    allowed_domains = ['dailythanthi.com']
    start_urls = ['https://www.dailythanthi.com/News/World/', 'https://www.dailythanthi.com/News/Puducherry/', 'https://www.dailythanthi.com/Sports/', 'https://www.dailythanthi.com/News/State/']

    def parse(self,response):
        lnkex = LinkExtractor(unique=True,strip=True)
        links = lnkex.extract_links(response)
        for link in links:
            yield scrapy.http.Request(link.url,callback=self.extract_info)
        
    
    def extract_info(self,response):
        #reponse.follow(link,callback=self.extract_info)
        Title =  response.css('.row').xpath('./p/text()').extract()
        Date = response.css('time ::text').extract()
        Article = response.css('.col-md-12').xpath('./div/text()').extract()

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
        
