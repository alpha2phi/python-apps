import scrapy


class ScraperSpider(scrapy.Spider):
    name = 'scraper'
    allowed_domains = ['investing.com']
    start_urls = ['http://investing.com/']

    def parse(self, response):
        pass
