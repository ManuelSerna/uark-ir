#*********************************
'''
SernaSpider
- A Mercator-inspired web crawler with pluggable components.

Call:
    $ python3 SernaSpider.py <max_pg>

<max_pg> is number of pages we wish to crawl

NOTE: This crawler should reasonably support 100,000 entries.
 It would not be efficient to process more URLs than that amount,
 at least without modifying the content-seen test data method. 
 As well as creating threads for each crawler.

Author: Manuel Serna-Aguilera
'''
#*********************************

# Imports
import Crawler # individual crawler component
import URLFrontier # url frontier component
import sys
import time



# Setup
max_pages = int(sys.argv[1]) # maximum pages to crawl (from cmd)

n_crawlers = 1 # equates to number of subqueues in frontier
queue_len = 500 # length of subqueues in frontier


# Provide list of starting URLs
# NOTE: an extra task would be to read links from txt file
start_urls = ['http://quotes.toscrape.com']

# Initialize URL frontier
frontier = URLFrontier.URLFrontier(n_subqueues=n_crawlers, len_subqueues=queue_len, start_urls=start_urls)


# Create crawler(s) list
crawlers = []
for i in range(n_crawlers):
    crawlers = crawlers + [Crawler.Crawler()]
#frontier.print_frontier()


#---------------------------------
# Crawl
#---------------------------------
print('Crawling at most {} pages.'.format(max_pages))
print()
start = time.time()

for t in range(max_pages):
    for i in range(len(crawlers)):
        # Get page url and crawl, get list of extracted links
        url = frontier.get_url(i)
        links = crawlers[i].crawl(url)
        
        # Insert urls, note that this method performs content-seen test in-method
        frontier.insert(links=links, verbose=True)
        
        print('---------------------------------')
        #frontier.print_frontier()

end = time.time()
elapsed = end - start
print()
print('Seconds elapsed:')
print('    %.6g' % elapsed)
print('Crawl complete.')
