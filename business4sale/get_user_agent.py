# import the required library
import scrapy
from scrapy.crawler import CrawlerProcess

class TutorialSpider(scrapy.Spider):
 
    # set the spider name
    name = "tutorial"
 
    # specify the target URL
    allowed_domains = ["httpbin.io"]
    start_urls = ["https://httpbin.io/headers"]
 
    # alter the user agent's platform with new custom headers
    custom_headers = {
            "Sec-Ch-Ua-Platform": "\"Linux\"",
            "User-Agent": "Mozilla/5.0 (Linux; x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            }
    # parse the response HTML
    def parse(self, response):
 
        # print the response text
        print(response.text)

if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(TutorialSpider)
    process.start()