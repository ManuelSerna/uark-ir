#*********************************
# Web Spider/Web Crawler using Scrapy
# This custom spider crawls websites and downloads the HTML pages into a subdirectory.
#
# Author: Manuel Serna-Aguilera
#*********************************

import re # for using regex
import scrapy

class MSASpider(scrapy.Spider):
    name = 'msa_spider' # name of spider
    
    # (Optional) Spider can only search within these domains
    #allowed_domains = []
    
    # Initialize URL domain
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]
    
    #-----------------------------
    # Settings for spider
    #-----------------------------
    SCHEDULER_PRIORITY_QUEUE = 'scrapy.pqueues.DownloaderAwarePriorityQueue' # Use recommended priority queue for broad crawls
    LOG_LEVEL = 'INFO' # Reduce clutter in console out
    COOKIES_ENABLED = False # Ignore cookies to not waste processing resources
    RETRY_ENABLED = False # If HTTP request fails once, never try again
    DOWNLOAD_TIMEOUT = 15 # Downloads of pages should take this many secs
    REDIRECT_ENABLED = False # Don't care about following redirects
    
    #-----------------------------
    # Extract HTML page contents when URL is crawled successfully
    # Input: response--result of crawling
    #-----------------------------
    def parse(self, response):
        print('crawling...{}'.format(response.url))
        
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
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)\

