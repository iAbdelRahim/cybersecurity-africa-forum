import scrapy
from caf.items import CafItem


class ScinapseSpider(scrapy.Spider):
    name = "scinapse"
    #allowed_domains = ["www.scinapse.io"]
    #start_urls = ["https://www.scinapse.io/search?query=cybersecurity&page=1&filter=year%3D%3A%2Cfield%3D%2Cvenue%3D&sort=RELEVANCE"]

    def start_requests(self):
        url = 'https://www.scinapse.io/search?query=cybersecurity&page=1&filter=year%3D%3A%2Cfield%3D%2Cvenue%3D&sort=RELEVANCE'
        yield SeleniumRequest(
                    url=url,
                    callback=self.parse,
                    wait_time=10,
                    wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'quote'))
                    )

    def parse(self, response):
        articles = response.xpath('/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-search-results/div/div[2]/div[2]')

        for article in articles:
            relative_url = article.css('p.list-title a ::attr(href)').get()
            if relative_url is not None:
                article_url = '' + relative_url
                yield response.follow(article_url, callback=self.parse)

        next_page = response.css('a.pagination-next ::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://ieeexplore.ieee.org/' + next_page
            yield response.follow(next_page_url, callback = self.parse)

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
