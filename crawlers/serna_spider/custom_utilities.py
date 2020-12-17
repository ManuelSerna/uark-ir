#*********************************
# My custom utilities module
#  This file contains several functions which may have use across
#  multiple components of SernaSpider.
# Author: Manuel Serna-Aguilera
#*********************************

# Imports
import hashlib
import random
import re
import time
import urllib
from urllib import parse
from urllib import robotparser
from urllib.parse import urlparse
from urllib.parse import urljoin


# Regex for regular URL; does not account for query parameters
url_regex = (
    "((http|https)://)(www.)?" +
    "[a-zA-Z0-9@:%._\\+~#?&//=]" +
    "{2,256}\\.[a-z]" +
    "{2,6}\\b([-a-zA-Z0-9@:%" +
    "._\\+~#?&//=]*)"
)

# Regex for URLs that do not have query parameters
url_noparams = "^((?:http:\/\/)|(?:https:\/\/))(www.)?((?:[a-zA-Z0-9]+\.[a-z]{3})|(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?::\d+)?))([\/a-zA-Z0-9\.]*)$"

# Regex for base URL
base_url_regex = "^(http:\/\/|https:\/\/)?([a-zA-Z0-9-_]+\.)*[a-zA-Z0-9][a-zA-Z0-9-_]+\.[a-zA-Z]{2,11}?$"

# Regex for special characters
special_chars = '[^A-Za-z0-9]+'

# Robots txt file name
robots = 'robots.txt'

#---------------------------------
# Make process sleep for t seconds
# Input: time t (seconds);
#        verbose is flag to print system time
# Return: NA
#---------------------------------
def delay(t=1, verbose=False):
    if verbose:
        print(' start: {}'.format(time.ctime()))
    time.sleep(t)
    if verbose:
        print(' end: {}'.format(time.ctime()))

#---------------------------------
# Use MD5 hashing to hash text
'''
Input:
    text: string to be hashed
Return: decimal integer representing hash of string
'''
#---------------------------------
def get_hash(text):
    return int(hashlib.md5(text.encode('utf-8')).hexdigest(), 16)

#---------------------------------
# Get base URL from given URL
'''
Input:
    url: some URL, may or may not be a base URL already
Return: 
    base URL, if nothing was found in given string,
     return None
'''
#---------------------------------
def get_base_url(url):
    if url == None:
        return False
    regex = re.compile(base_url_regex)
    result = regex.search(url)
    if result == None:
        return None
    return result.group(0)
    

#---------------------------------
# Check if given url is in valid format (i.e. it is not broken)
#  compare against regular exp.
'''
Input:
    url: string representation of URL
Return:
    Boolean whether url matches regular
'''
#---------------------------------
def is_valid_url(url):
    if url == None:
        return False
    #regex = re.compile(url_regex)# get regex object
    regex = re.compile(url_noparams)
    if re.search(regex, url): # run string through regex
        return True
    else:
        return False

#---------------------------------
# Check if given url is crawable by checking robots.txt
'''
Input:
    cand_path: candidate path, string
    base: base url, string
    rp: robot parser, urllib.robotparser object
Return: Boolean
'''
#---------------------------------
def is_crawable_subpath(cand_path='', base='', rp=None, verbose=False):
    # Throw out nones and empty strings
    if cand_path == None or cand_path == '' or base == None or base == '':
        return False
    
    # If here, we may have a valid URL path
    if cand_path[0] == '/':
        full_path = base + cand_path # full url (base url + subpath, which may be crawable)
        robots_path = base + '/' + robots # directory for robots.txt
        try:
            rp.set_url(robots_path)
            rp.read()
            can_crawl = rp.can_fetch('*', full_path)
            if verbose:
                print('  Crawl "{}" {}!'.format(full_path, can_crawl))
            return can_crawl
        except:
            return False # return false if any error occurs
    else:
        return False
    

#---------------------------------
# Remove special characters from string
'''
Input: input text
Return: input text but with special characters removed
'''
#---------------------------------
def remove_spec_chars(text):
    return re.sub(special_chars, '', text) # regex, replacement str, input text
