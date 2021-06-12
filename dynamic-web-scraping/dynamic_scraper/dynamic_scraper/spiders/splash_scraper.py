import re
import scrapy
from scrapy.selector import Selector
from scrapy_splash import SplashRequest


class SplashScraperSpider(scrapy.Spider):
    name = 'splashscraper'
    allowed_domains = ['investing.com']
    start_urls = [
        'https://www.investing.com/equities/google-inc-c-balance-sheet'
    ]

    # Lua script to click the button
    script = r"""
    function main(splash, args)
        assert(splash:go(args.url))
        assert(splash:wait(1))

        js = string.format(
            "document.querySelector(\"a[data-ptype='Annual']\").click();", args.page)
        splash:runjs(js)
        assert(splash:wait(1))
        return splash:html()
    end
    """

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,
                                self.parse,
                                endpoint='execute',
                                args={
                                    'wait': 10,
                                    'images': 0,
                                    'lua_source': self.script
                                })

    def parse(self, response):
        selector = Selector(response)
        elements = selector.xpath(
            "//*[@id='rrtable']/table//*[@id='header_row']/th/span")
        for element in elements:
            text = element.extract()
            match = re.search(r"\d\d\d\d", text.strip())
            if match:
                self.log(match.group(0))
