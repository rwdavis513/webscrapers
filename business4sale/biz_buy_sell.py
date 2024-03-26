import scrapy
import json, os
from constants import DATA_FOLDER
from datetime import datetime
from urllib.parse import urlsplit


if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

def get_filename_from_url(url=None):
    if url is None:
        return None
    urlpath = urlsplit(url).path
    return urlpath.replace('/', '__')


def test_get_filename_from_url():
    url = "https://gabrieleromanato.name/python-how-to-extract-the-file-name-from-a-url"
    filename = get_filename_from_url(url)
    print(filename)


def save_object_to_file(object_, url):
    today = datetime.now().isoformat()
    file_name = get_filename_from_url(url) + today
    file_path = os.path.join(DATA_FOLDER, file_name + '.json')
    json.dump(object_, open(file_path, 'w'))
    return file_path

def try_except(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            return None
    return wrapper

@try_except
def get_css(css_selector, block):
    text = block.css(css_selector).get()
    if text:
        return text.strip()
    else:
        return None


def get_cashflow(block):
    text = get_css('p.cash-flow.show-on-mobile.ng-star-inserted::text', block)
    if isinstance(text, str):
        return text.replace("Cash Flow: ", "")
    else:
        return text


# 'title': block.css('a').attrib["title"],
# 'link': block.css('a').attrib["href"],
# 'asking_price': block.xpath('//*[@id="2175771"]/div/div[2]/p[1]/text()').get(),
# 'cashflow': block.xpath('//*[@id="2175771"]/div/div[2]/p[2]/text()').get().replace("Cash Flow: ",""),
# 'location': block.css('p.location.ng-star-inserted::text').get().strip(),
# 'image': block.css('div.ng-img-container > img::attr(src)').get(),
# 'description': block.css('p.description.ng-star-inserted::text').get(), 

#base_url = 'https://www.bizbuysell.com/utah-businesses-for-sale/'

#base_url = 'https://www.bizbuysell.com/utah-established-businesses-for-sale/' #?q=Y2Zmcm9tPTUwMDAw
base_url = 'https://www.bizbuysell.com/utah-established-businesses-for-sale/'
class BizBuySellSpider(scrapy.Spider):
    name = "BizBuySell"
    allowed_domains = ['bizbuysell.com']
    
    start_urls = ['{}{}/?q=Y2Zmcm9tPTUwMDAwJmkyPTExOCwzMSw1NywxMTU%3D'.format(base_url, i) for i in range(1, 2) ]

    def parse(self, response):
        
        results = []
        selectors = (
            response.css('#search-results > app-bfs-listing-container > div > app-listing-diamond'),
            response.css('#search-results > app-bfs-listing-container > div > app-listing-showcase'),
            response.css('#search-results > app-bfs-listing-container > div > app-listing-basic')
        )
        for items in selectors:
            for block in items:
                
                item = {
                    'title': get_css('a::attr(title)', block), #block.css('a').attrib["title"],
                    'link': get_css('a::attr(href)', block), #block.css('a').attrib["href"],
                    'asking_price': get_css('p.asking-price.ng-star-inserted::text', block), #block.xpath('//*[@id="2175771"]/div/div[2]/p[1]/text()
                    'cashflow': get_cashflow(block), #block.xpath('//*[@id="2175771"]/div/div[2]/p[2]/text()').get().replace("Cash Flow: ",""),
                    'location': get_css('p.location.ng-star-inserted::text', block), #block.css('p.location.ng-star-inserted::text').get().strip(),
                    'image': get_css('div.ng-img-container > img::attr(src)', block), #block.css('div.ng-img-container > img::attr(src)').get(),
                    'description': get_css( 'p.description.ng-star-inserted::text', block), #block.css('p.description.ng-star-inserted::text').get(), # .css('p.description.ng-star-inserted::text').get()
                }
                results.append(item)
                #yield item 
        save_object_to_file(results, response.url)


if __name__ == "__main__":
    test_get_filename_from_url()