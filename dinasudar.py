# -*- coding: utf-8 -*-
import scrapy
import hashlib
from scrapy.linkextractors import LinkExtractor


class DinasudarSpider(scrapy.Spider):
    name = 'dinasudar'
    allowed_domains = ['dinasudar.co.in']
    start_urls = ['http://dinasudar.co.in/']

    def parse(self,response):
        lnkex = LinkExtractor(unique=True,strip=True)
        links = lnkex.extract_links(response)
        for link in links:
            yield scrapy.http.Request(link.url,callback=self.extract_info)
        
    
    def extract_info(self,response):
        #reponse.follow(link,callback=self.extract_info)
        Title =   response.css('h1::text').extract()
        Date =  response.css('time::text').extract()[0]
        Article = response.css('.td-post-content').xpath('p/text()').extract()
 



        text = ""
        title = ""
        date_time = ""
                
        for para in Article:
            text = text + "\n" +para

        for sent in Title:
            #sent = ''.join(Title).encode('utf-8').strip('\r\t\n')
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
         
