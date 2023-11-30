import scrapy
import re
from caf.items import CafItem


class GscholarSpider(scrapy.Spider):
    name = "gscholar"
    allowed_domains = ["scholar.google.com"]
    start_urls = ["https://scholar.google.com/scholar?start=980&q=cybersecurity&hl=fr&as_sdt=0,5&as_vis=1"]

    def parse(self, response):
        articles = response.css('.gs_ri')
        caf_item = CafItem()

        for article in articles:
            caf_item['link'] = article.css('.gs_rt a ::attr(href)').getall()
            caf_item['authors'] = article.css('.gs_a ::text').getall()
            receive = str("".join(str(elem) for elem in (caf_item['authors'])))
            year = "".join(str(elem) for elem in re.findall('\d', receive))
            if len(year) != 4:
                string = "01" + year
            else:
                string = "01" + " Jan " + year
            caf_item['pub_date'] = string
            caf_item['title'] = article.css('.gs_rt a ::text').getall()
            caf_item['abstract'] = article.css('.gs_rs ::text').getall()
            caf_item['subjects'] = "COMPUTER SCIENCE"
            yield caf_item

        next_page = response.css('td[align="left"][nowrap] a ::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://scholar.google.com' + next_page
            yield response.follow(next_page_url, callback=self.parse)

"""
    def parse(self, response):
        articles = response.css('.gs_ri')

        for article in articles:
            yield{
                'title': article.css('.gs_rt a ::text').getall(),
                'link': article.css('.gs_rt a::attr(href)').get(),
                'source': article.css('.gs_a ::text').getall(),
                'abstract': article.css('.gs_rs ::text').getall()
            }
        next_page = response.css('td[align="left"][nowrap] a ::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://scholar.google.com' + next_page
            yield response.follow(next_page_url, callback = self.parse)
"""
"""
    def parse(self, response):
        articles = response.css('.gs_ri')
        caf_item = CafItem()

        for article in articles:
            caf_item['link'] = article.css('.gs_rt a ::text').getall()
            caf_item['pub_date'] = article.css('.gs_a ::text').getall()
            caf_item['title'] = article.css('.gs_rt a ::text').getall()
            caf_item['authors'] = article.css('.gs_a ::text').getall()
            caf_item['abstract'] = article.css('.gs_rs ::text').getall()
            caf_item['subjects'] = ""
            yield caf_item

        next_page = response.css('td[align="left"][nowrap] a ::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://scholar.google.com' + next_page
            yield response.follow(next_page_url, callback=self.parse)
"""

