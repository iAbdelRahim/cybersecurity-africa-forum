import scrapy


class ArxivSpider(scrapy.Spider):
    name = "arxiv"
    allowed_domains = ["arxiv.org"]
    start_urls = ["https://arxiv.org/search/?query=cybersecurity&searchtype=all&abstracts=show&order=-announced_date_first&size=50"]

    def parse(self, response):
        articles = response.css('li.arxiv-result')

        for article in articles:
            yield{
                'title': article.css('p.title ::text').getall(),
                'link': article.css('p.list-title a ::attr(href)').getall(),
                'authors': article.css('p.authors ::text').getall(),
                'abstract': article.css('p.abstract ::text').getall(),
                'submitted': article.css('p.is-size-7 ::text').getall()
            }
        next_page = response.css('a.pagination-next ::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://arxiv.org/' + next_page
            yield response.follow(next_page_url, callback = self.parse)