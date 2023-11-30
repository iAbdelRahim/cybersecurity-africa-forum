import scrapy
from caf.items import CafItem
import random

class Arxiv2Spider(scrapy.Spider):
    name = "arxiv2"
    allowed_domains = ["arxiv.org"]
    start_urls = ["https://arxiv.org/search/?query=cybersecurity&searchtype=all&abstracts=show&order=-announced_date_first&size=50"]

    # user_agent_list = [
    #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    #     'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    #     'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    # ]

    def parse(self, response):
        articles = response.css('li.arxiv-result')

        for article in articles:
            relative_url = article.css('p.list-title a ::attr(href)').get()
            if relative_url is not None:
                article_url = '' + relative_url
                # yield response.follow(article_url, callback=self.parse,
                #        headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]})
                yield response.follow(article_url, callback=self.parse_article)

        next_page = response.css('a.pagination-next ::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://arxiv.org/' + next_page
            # yield response.follow(next_page_url, callback = self.parse,
            #            headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]})
            yield response.follow(next_page_url, callback=self.parse)

    def parse_article(self, response):
        article = response.css('#content-inner')
        caf_item = CafItem()

        caf_item['link'] = response.url
        caf_item['pub_date'] = article.css('.dateline ::text').get()
        caf_item['title'] = article.css('h1.title ::text').getall()
        caf_item['authors'] = article.css('.authors ::text').getall()
        caf_item['abstract'] = article.css('.abstract ::text').getall()
        caf_item['subjects'] = article.css('td.tablecell.subjects ::text').getall()
        yield caf_item