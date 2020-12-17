#*********************************
# Web Spider/Web Crawler using Scrapy
# This custom spider crawls websites and downloads the HTML pages into a subdirectory.
#
# Author: Manuel Serna-Aguilera
#*********************************

import re # for using regex
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import urllib




class MSASpider(CrawlSpider):
    name = 'msa_spider' # name of spider
    
    # (Optional) Spider can only search within these domains
    #allowed_domains = []
    
    # Initialize URL list
    start_urls = [
        'http://quotes.toscrape.com'
    ]
    
    # Settings for spider
    # Taken from docs: https://docs.scrapy.org/en/latest/topics/broad-crawls.html
    custom_settings = {
        'SCHEDULER_PRIORITY_QUEUE': 'scrapy.pqueues.DownloaderAwarePriorityQueue', # Use recommended priority queue for broad crawls
        'CONCURRENT_REQUESTS': 100, # global concurrency limit increased for broad crawl
        'REACTOR_THREADPOOL_MAXSIZE': 20, # increase threads used in DNS resolutions
        'LOG_LEVEL': 'INFO', # Reduce clutter in console out
        'COOKIES_ENABLED': False, # Ignore cookies to not waste processing resources
        'RETRY_ENABLED': False, # If HTTP request fails once, never try again
        'DOWNLOAD_TIMEOUT': 15, # Downloads of pages should take this many secs
        'REDIRECT_ENABLED': False # Don't care about following redirects
    }
    
    
    # Rules for spider, which will allow for Scrapy to follow any link it finds
    rules = [Rule(LinkExtractor(), callback='parse', follow=True)]
    
    #-----------------------------
    # Extract HTML page contents
    #-----------------------------
    def parse(self, response):
        print('  crawling...{}'.format(response.url))
        
        # Get raw HTML code
        html_content = response.xpath('//*').get() # get everything
        
        # Write plain text HTML to file in subdirectory
        downloads_dir = 'downloads/'
        page_name = re.sub('[^A-Za-z0-9]+', '', response.url)
        ext = '.html'
        full_path = downloads_dir + page_name + ext # build full path for file
        page = open(full_path, 'w')
        page.write(html_content)
        page.close()
        
        # Crawl more pages if they exist
        next_page = response.css('li.next a::attr(href)').get()
        
        if next_page is not None:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
