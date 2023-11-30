import scrapy
import re
from scrapy_splash import SplashRequest
from caf.items import CafItem


class SciencedirectSpider(scrapy.Spider):
    name = "scienceDirect"
    allowed_domains = ["www.sciencedirect.com"]
    start_urls = ["https://www.sciencedirect.com/search?qs=cybersecurity"]

    def parse(self, response):
        articles = response.css('.result-item-content')

        for article in articles:
            relative_url = article.css('h2 a.result-list-title-link ::attr(href)').get()
            if relative_url is not None:
                article_url = '' + relative_url
                yield SplashRequest(article_url, callback=self.parse_article, args={'wait': 120})

        next_page = response.css('li.next-link a.anchor ::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://www.sciencedirect.com/' + next_page
            yield SplashRequest(article_url, callback=self.parse, args={'wait': 120})

    def parse_article(self, response):
        article = response.css('article')
        caf_item = CafItem()

        def extract_received_date(text):
            # Extract the date from the "Received" field
            match = re.search(r"Received (\d+ \w+ \d+)", text)
            if match:
                return match.group(1)
            else:
                return None

        caf_item['link'] = response.url
        authors = response.css('#author-group')
        for author in authors:
            single = author.css('span.react-xocs-alternative-link')
            caf_item['authors'] = "".join(str(elem) for elem in single)

        caf_item['pub_date'] = extract_received_date(article.css('.dateline ::text').get())
        caf_item['title'] = article.css('#screen-reader-main-title span.title-text ::text').getall()
        # caf_item['authors'] = article.css('.authors ::text').getall()
        caf_item['abstract'] = article.css('#abstracts ::text').getall()
        caf_item['subjects'] = article.css('div.keywords-section').getall()
        yield caf_item
