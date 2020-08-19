import scrapy
import requests
import base64
import logging
from scrapy.http import FormRequest
from scrapy.exceptions import CloseSpider
from scrapy.loader import ItemLoader
from tutorial.items import FbcrawlItem, parse_date, parse_date2
from datetime import datetime


def get_as_base64(url):
    return base64.b64encode(requests.get(url).content)


class PostSpider(scrapy.Spider):
    name='post'
    def __init__(self):
        self.email = 'haohoang3100@gmail.com'
        self.password = '123456789hao'
        self.start_urls = ['https://mbasic.facebook.com']

    def parse(self, response):
        return FormRequest.from_response(
            response,
            formxpath='//form[contains(@action, "login")]',
            formdata={'email': self.email, 'pass': self.password},
            callback=self.parse_page
        )

    def parse_page(self, response):
        href = "https://mbasic.facebook.com/groups/284674951892342?view=permalink&id=1258737917819369"
        return scrapy.Request(url=href, callback=self.parse_post2, meta={'index': 1})

    # def parse_post1(self, response):
    #     from scrapy.utils.response import open_in_browser
    #     open_in_browser(response)
    #     for post in response.xpath("//article[contains(@data-ft,'top_level_post_id')]"):
    #         full_story = post.xpath(".//a[contains(@href,'footer')]/@href").extract()
    #         temp_post = response.urljoin(full_story[0])
    #         yield scrapy.Request(temp_post, self.parse_post2)

    def parse_post2(self, response):
        from scrapy.utils.response import open_in_browser
        open_in_browser(response)
        new = ItemLoader(item=FbcrawlItem(), selector=response)
        # new.add_value('post_id', '3247974425299401')
        new.add_xpath('text', "//div[contains(@data-ft, 'top_level_post_id')]//p//text() | //div[@data-ft]/div[@class]/div[@class]/text() | //div[contains(@data-ft, 'top_level_post_id')]//span[@style]/text()")
        image_source = response.xpath(
            "//div[contains(@data-ft, 'top_level_post_id')]//a[contains(@href, 'photo')]/img/@src")
        encodes = list()
        for src in image_source.getall():
            code = get_as_base64(src)
            encodes.append(code)
        new.add_value('image', encodes)
        return new.load_item()
