#*********************************
# Custom Spider for collecting new web pages
#*********************************
# https://dev.to/pranay749254/build-a-simple-python-web-crawler
import requests
from bs4 import BeautifulSoup



class SernaSpider():
    # Input: (Python list) starting URLs
    def __init__(self, start_urls):
        self.start_urls = start_urls
    
    # Crawl pages in frontier
    def crawl(self):
        # TODO
        print('crawling...')
