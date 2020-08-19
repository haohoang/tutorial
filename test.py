# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
#
# process = CrawlerProcess(get_project_settings())
#
# # 'followall' is the name of one of the spiders of the project.
# process.crawl('test', {"last": "last_page_1.txt"})
# process.start() # the script will block here until the crawling is finished


import requests
import base64

response = requests.get("https://scontent.fhan2-4.fna.fbcdn.net/v/t1.0-0/cp0/e15/q65/p320x320/81523047_254381455524514_3157121495969300480_n.jpg?_nc_cat=105&_nc_sid=07e735&_nc_ohc=G-mwSl5THJoAX-IXBlA&_nc_ht=scontent.fhan2-4.fna&tp=3&oh=512d606766331ca71602ad6030ebbdb3&oe=5F630B0B").content
uri = ("data:" +
       'image/jpeg' + ";" +
       "base64," + base64.b64encode(response).decode("utf-8"))

print(type(uri))