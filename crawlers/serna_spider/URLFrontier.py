#*********************************
# Component for URL frontier
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
        
        # Init URL frontier with empty subqueues
        for i in range(self.n_subqueues):
            self.frontier = self.frontier + [Queue.Queue(length=self.len_subqueues)]
        
        # Populate frontier with given starting URL list
        n_start = len(start_urls)
        i = 0 # index for frontier
        
        for j in range(n_start):
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
    # Print contents of frontier (for debugging)
    # Input: NA
    # Return: NA
    #=============================
    def print_frontier(self):
        for i in range(self.n_subqueues):
            print(self.frontier[i].print_queue())
