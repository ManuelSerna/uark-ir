#*********************************
# Driver code for custom spider class
#*********************************

# Imports
import spider
from spider import SernaSpider



# Setup
# Start with the below link, there should only be 10 pages. After successfully crawling the ten pages, make spider more attack-robust and crawl more sites
start_urls = [
    'http://quotes.toscrape.com/page/1/'
]



# Test crawling
my_spider = SernaSpider(start_urls)
my_spider.crawl()
