#*********************************
'''
    SernaSpider
    - A Mercator-inspired web crawler with pluggable components.
    
    Author: Manuel Serna-Aguilera
'''
#*********************************

# Imports
import Crawler # individual crawler component
import URLFrontier # url frontier component



#---------------------------------
# Setup
#---------------------------------

# Provide list of starting URLs
# NOTE: an extra task would be to read links from txt file
# TEMP NOTE: Start with the below link, there should only be 10 pages. After successfully crawling the ten pages, make spider more attack-robust and crawl more sites

start_urls = ['http://quotes.toscrape.com/page/1/']

#start_urls = ['https://soundcloud.com/'] # soundcloud allows crawling, apparently

#start_urls = ['https://en.wikipedia.org/wiki/Web_scraping']

# Initialize URL frontier
num_spiders = 1 # equates to number of subqueues in frontier
queue_len = 100
frontier = URLFrontier.URLFrontier(n_subqueues=num_spiders, len_subqueues=queue_len, start_urls=start_urls)

# Create crawler(s)
crawlers = []
for i in range(num_spiders):
    crawlers = crawlers + [Crawler.Crawler()]

#frontier.print_frontier()

# Crawl
i=0
url = frontier.get_url(i)
links = crawlers[i].crawl(url, True)

# Resolve duplicate URLs in returned list
# TODO: 
raise Exception(' after crawling, iterate over links list and filter out already-existing urls that have been crawled!')

# TODO: then, crawl again
##

# TODO: loop for some amount of time or set num of pages
##

#print(links) # TEST: print extracted valid links
print('printing retrieved links')
for link in links:
    print(link)
