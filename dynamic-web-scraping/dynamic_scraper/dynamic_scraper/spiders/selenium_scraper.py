import re
import scrapy
from scrapy.selector import Selector


class SeleniumScraperSpider(scrapy.Spider):
    name = 'seleniumscraper'
    allowed_domains = ['investing.com']
    start_urls = [
        'https://www.investing.com/equities/google-inc-c-balance-sheet'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        selector = Selector(response)
        elements = selector.xpath(
            "//*[@id='rrtable']/table//*[@id='header_row']/th/span")
        for element in elements:
            text = element.extract()
            match = re.search(r"\d\d\d\d", text.strip())
            if match:
                self.log(match.group(0))
