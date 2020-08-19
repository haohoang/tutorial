import scrapy
from scrapy.http import FormRequest


class VNWorkSpider(scrapy.Spider):
    name = 'vietnamwork'

    # def __init__(self, **kwargs):
    #     super(VNWorkSpider, self).__init__(**kwargs)
    #     self.email = 'learnopencvforfun@gmail.com'
    #     self.password = 'Learn0penCV'
    #     self.page = "https://www.vietnamworks.com/viec-lam-ha-noi-v24-vn"
    #     # self.start_urls = ['https://secure.vietnamworks.com/login/en?client_id=3']

    start_urls = [
        "https://www.careerlink.vn/tim-viec-lam/giam-doc-thanh-tra-chat-luong-dich-vu-qa-qc-mang-ban-le/1816000"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-1] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
    # def parse(self, response):
    #     from scrapy.utils.response import open_in_browser
    #     open_in_browser(response)
    #     return FormRequest.from_response(
    #         response,
    #         formxpath='//form[contains(@action, "login")]',
    #         formdata={'email': self.email, 'pass':self.password},
    #         callback=self.parse_home
    #     )

    def parse_home(self, response):
        print("Login thanh cong")
        return scrapy.Request(url=self.page, callback=self.parse_page, meta={'index': 1})

    def parse_page(self, response):
        from scrapy.utils.response import open_in_browser
        open_in_browser(response)
        for post in response.xpath("//div[contains(@class, 'container-fluid')]"):
            url = post.xpath("//h3/a/@href").extract()
            print(url)
            path = response.urljoin(url[0])
            yield scrapy.Request(path, self.parse_job)

    def parse_job(self, response):
        from scrapy.utils.response import open_in_browser
        open_in_browser(response)
