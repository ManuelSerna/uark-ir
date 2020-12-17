#*********************************
# Component for URL frontier
# Author: Manuel Serna-Aguilera
#*********************************

import Queue # custom queue module

class URLFrontier():
    #=============================
    # Init
    '''
    Input:
        n_subqueues: number of subqueues the frontier will contain (same number as spiders)
        len_subqueues: length of each subqueue
        start_urls: list of URLs to start crawl from
    '''
    #=============================
    def __init__(self, n_subqueues=1, len_subqueues=100, start_urls=[]):
        # Init attributes
        self.n_subqueues = n_subqueues
        self.len_subqueues = len_subqueues
        self.frontier = [] # Q is a python list of constant size
        self.content = {} # keep list of urls for content-seen test
        self.max_urls = 100000 # max number of 
        self.unique_urls = len(start_urls) # number of unique urls found so far [1...100000]
        
        # Init URL frontier with empty subqueues
        for i in range(self.n_subqueues):
            self.frontier = self.frontier + [Queue.Queue(length=self.len_subqueues)]
        
        # Populate frontier with given starting URL list, and init content-seen
        i = 0 # index for frontier
        for j in range(self.unique_urls):
            self.content[start_urls[i]] = 1
            self.frontier[i].enqueue(start_urls[j])
            i += 1
            if i == self.n_subqueues:
                i = 0
    
    #=============================
    # Get a URL at a certain index
    '''
    Input:
        index: index for subqueue we wish to dequeue URL from
    Return: 
        url: dequeued element (may or may not be 'None')
    '''
    #=============================
    def get_url(self, index):
        url = self.frontier[index].dequeue()
        return url
    
    #=============================
    # Insert list of urls evenly into frontier
    '''
    Input:
        links: list of urls
    Return: NA
    
    NOTE: content-seen test is done here
    '''
    #=============================
    def insert(self, links=[], verbose=False):
        n = len(links)
        i = 0 # frontier index
        for j in range(n):
            ###Check for trailing forward slash, and remove if present
            #if links[j][-1] != '/':
            #links[j] = links[j] + '/'
            
            # Only insert if url has not been seen before
            if not self.content_seen(links[j]):
                self.frontier[i].enqueue(links[j])
                if verbose:
                    print(' New: {}'.format(links[j]))
            i += 1
            if i == self.n_subqueues:
                i = 0
    
    #=============================
    # Perform content-seen test on url
    '''
    Input:
        url: single absolute url
    Return: boolean (is url in content dictionary?)
    '''
    #=============================
    def content_seen(self, url):
        if url in self.content:
            # If url exists in dictionary, add count and return true
            self.content[url] += 1
            return True
        else:
            # URL brand new, add it to dictionary and return false
            self.content[url] = 1
            return False
    
    #=============================
    # Print contents of frontier (for debugging)
    # Input: NA
    # Return: NA
    #=============================
    def print_frontier(self):
        for i in range(self.n_subqueues):
            print(self.frontier[i].print_queue())
