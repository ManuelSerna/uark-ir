#*********************************
# Crawler component of SernaSpider
# Author: Manuel Serna-Aguilera
#*********************************

# Imports
import bs4 # dummy placeholder name of BeautifulSoup (actually imported below)
from bs4 import BeautifulSoup
import random
import requests
import urllib
from urllib import parse
from urllib import robotparser
from urllib.parse import urlparse
from urllib.parse import urljoin

# My module(s)
import custom_utilities as myutils



class Crawler():
    #=============================
    # Init
    '''
    Input:
        downloads_dir: directory where fetched HTML documents will be stored.
    Return: NA
    '''
    #=============================
    def __init__(self, downloads_dir='downloads/'):
        self.SIZE_LIMIT = 20 # max number of links allowed to be retrieved        
        self.downloads_dir = downloads_dir
        self.connection_time = 2.5 # max time to allow requests to wait on connection
        self.reponse_time = 2.5
        
        # Declare robot parser
        self.rp = robotparser.RobotFileParser()
        
        # User agent used in requesting pages
        self.agent_name = 'MSA'
    
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
    '''
    # NOTE: This method assumes url is crawable and will download page 
        associated with url (if request was successful).
    # NOTE: This method filters out duplicate URLs, URLs
    
    Input:
        url: given (single) URL for crawler to look up. It is assumed URL is valid.
        verbose: output extra lines to keep track of what is being processed.
    Return:
        links: list of found URLs
    '''
    #=============================
    def crawl(self, url=None, verbose=False):
        links = [] # init empty list of found URLs
        
        if url == None:
            return links # return empty list if url is empty variable
        
        # Sleep for random t seconds before making request to avoid overloading
        t = random.randint(15, 30)
        if verbose:
            print('Delaying request for {} secs.'.format(t))
        myutils.delay(t=t, verbose=verbose)
        
        # Request page. Time out secs set in constructor.
        r = None
        try:
            r = requests.get(url, timeout=(self.connection_time, self.reponse_time))
        except:
            return links # if any error in request was made, return empty list
        
        if verbose:
            print('_______________________________________')
            print('Crawling url: {}'.format(url))
            print(' status code: {}'.format(r.status_code))
        
        # Process page only if request was successful
        if r.status_code == 200:
            page = BeautifulSoup(r.text, 'html.parser') # get html
            
            # Iterate and only get valid URLs
            for href in page.find_all('a'):
                link = href.get('href') # get extracted link from HTML
                
                # Check if subpath of current URL is crawable
                base = myutils.get_base_url(url)
                #raise Exception('in below line, replace url with base')
                if myutils.is_crawable_subpath(link, base, self.rp):
                    links.append(url+link)
                    continue # don't wanna add link twice
                
                # Check if looking at external URL
                if myutils.is_valid_url(link):
                    if verbose:
                        print(link)
                    links.append(link)
            
            # Write page to file (regardless of how many links were extracted)
            self.write_html_to_file(page, url)
        
        # If there's too many links, choose random subset
        #if len(links) > self.SIZE_LIMIT:
        #    links = random.choices(links, k=self.SIZE_LIMIT)
        
        if verbose:
            print('  links extracted={}'.format(len(links)))
        
        return links
