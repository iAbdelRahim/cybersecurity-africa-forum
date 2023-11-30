import scrapy
from caf.items import CafItem
from scrapy_selenium import SeleniumRequest
"""
class IeeeSpider(scrapy.Spider):
    name = "ieee"
    #allowed_domains = ["ieeexplore.ieee.org"]
    #start_urls = ["https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=cybersecurity"]

    def start_requests(self):
        url = 'https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=cybersecurity'
        yield SeleniumRequest(url=url, callback=self.parse)


    def parse(self, response):
        articles = response.xpath('/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-search-results/div/div[2]/div[2]')

        def parse(self, response):
            articles = response.css('div.space-y-4 div.space-y-2 div.relative.flex')

            for article in articles:
                relative_url = article.css('div.space-y-4 div.space-y-2 div.space-y-2 div.w-full a ::attr(href)').get()
                if relative_url is not None:
                    article_url = '' + relative_url
                    yield response.follow(article_url, callback=self.parse)

            next_page = response.css('a.pagination-next ::attr(href)').get()
            if next_page is not None:
                next_page_url = 'https://arxiv.org/' + next_page
                yield response.follow(next_page_url, callback=self.parse)

        def parse_article(self, response):
            article = response.xpath('/html/body/div[1]/main/div/div[1]/div/div[1]/div')
            caf_item = CafItem()

            caf_item['link'] = response.url
            caf_item['pub_date'] = article.xpath(
                '/html/body/div[1]/main/div/div[1]/div/div[1]/div/div[1]/div[3]/div[3]/text()[2]').getall()
            caf_item['title'] = article.xpath(
                '/html/body/div[1]/main/div/div[1]/div/div[1]/div/div[4]/div[2]/div[2]').getall()
            caf_item['authors'] = article.xpath(
                '/html/body/div[1]/main/div/div[1]/div/div[1]/div/div[1]/div[2]/div').getall()
            caf_item['abstract'] = article.xpath(
                '/html/body/div[1]/main/div/div[1]/div/div[1]/div/div[2]/div[2]/span/text()').getall()
            caf_item['subjects'] = article.xpath(
                '/html/body/div[1]/main/div/div[1]/div/div[1]/div/div[3]/div[2]').getall()
            yield caf_item"""

class IeeeSpider(scrapy.Spider):
    name = "ieee"
    #allowed_domains = ["ieeexplore.ieee.org"]
    #start_urls = ["https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=cybersecurity"]

    def start_requests(self):
        url = 'https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=cybersecurity'
        yield SeleniumRequest(url=url, callback=self.parse)


    def parse(self, response):
        articles = response.css('xpl-results-item')
        caf_item = CafItem()

        for article in articles:
                caf_item['title']: article.css('div.col.result-item-align.px-3').getall()
                caf_item['link']: article.css('p.list-title a ::attr(href)').getall()
                caf_item['authors']: article.css('p.authors ::text').getall()
                caf_item['abstract']: article.css('p.abstract ::text').getall()
                caf_item['submitted']: article.css('p.is-size-7 ::text').getall()

        next_page = response.css('a.pagination-next ::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://arxiv.org/' + next_page
            yield response.follow(next_page_url, callback = self.parse)