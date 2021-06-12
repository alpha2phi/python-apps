import re
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SeleniumScraperSpider(scrapy.Spider):
    name = 'seleniumscraper'
    allowed_domains = ['investing.com']
    start_urls = [
        'https://www.investing.com/equities/google-inc-c-balance-sheet'
    ]

    CHROME_DRIVER = '/Users/mengwangk/workspace/software/webdriver/chromedriver'

    def start_requests(self):
        self.driver = webdriver.Chrome(self.CHROME_DRIVER)
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.driver.get(response.url)
        btn = self.driver.find_element_by_css_selector(
            "a[data-ptype='Annual']")
        btn.click()

        WebDriverWait(self.driver, 300).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "table[class='genTbl reportTbl']")))

        elements = self.driver.find_elements_by_xpath(
            "//*[@id='rrtable']/table//*[@id='header_row']/th/span")

        for element in elements:
            text = element.get_attribute("innerText")
            match = re.search(r"\d\d\d\d", text.strip())
            if match:
                self.log(match.string)
