#*********************************
# Crawler component of SernaSpider
# Author: Manuel Serna-Aguilera
#*********************************

# Imports
import bs4 # dummy placeholder name of BeautifulSoup (actually imported below)
from bs4 import BeautifulSoup
import requests

# My module(s)
import custom_utilities as myutils



class Crawler():
    #=============================
    # Init
    '''
    Input:
        downloads_dir: directory where fetched HTML documents will be stored.
    '''
    #=============================
    def __init__(self, downloads_dir='downloads/'):
        self.SIZE_LIMIT = 25 # max number of links allowed to be retrieved
        self.downloads_dir = downloads_dir
        self.connection_time = 2.5 # max time to allow requests to wait on connection
        self.reponse_time = 2.5
    
    #=============================
    # Write HTML contents to file
    '''
    Input:
        page: BeautifulSoup object containing HTML page information
        url: will be used as the file name (after removing special chars)
    Return: NA
    '''
    #=============================
    def write_html_to_file(self, page, url):
        file_name = self.downloads_dir + myutils.remove_spec_chars(url) + '.html'
        out_file = open(file_name, 'w')
        out_file.write(str(page))
        out_file.close()
    
    #=============================
    # Crawl a single page; extract other URLs
    # NOTE: this method filters out duplicate URLs
    '''
    Input:
        url: given (single) URL for crawler to look up.
            It is assumed URL is valid.
    Return:
        links: list of found URLs
    '''
    #=============================
    def crawl(self, url=None, verbose=False):
        links = [] # init empty list of found URLs
        
        if url == None:
            return links # return empty list if url is '
        
        # Sleep for some seconds before making request to avoid overloading; 
        #  then make requests with time limits on connection and response time.
        myutils.delay(t=10, verbose=verbose)
        r = requests.get(url, timeout=(self.connection_time, self.reponse_time))
        
        if verbose:
            print('_______________________________________')
            print('Crawling url...{}'.format(url))
            print('  status code: {}'.format(r.status_code))
        
        # Process page only if request was successful
        if r.status_code == 200:
            page = BeautifulSoup(r.text, 'html.parser')
            
            # Iterate and only get valid URLs
            for href in page.find_all('a'):
                link = href.get('href')
                if myutils.is_valid_url(link):
                    if verbose:
                        print(link)
                    links.append(link)
            
            # Write page to file
            self.write_html_to_file(page, url)
        
        if verbose:
            print('  links extracted={}'.format(len(links)))
        
        return links
