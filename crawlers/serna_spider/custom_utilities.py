#*********************************
# My custom utilities module
#  This file contains several functions which may have use across
#  multiple components of SernaSpider.
# Author: Manuel Serna-Aguilera
#*********************************

# Imports
import hashlib
import re # regular expression
import time


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

# Regex for 
special_chars = '[^A-Za-z0-9]+'

#---------------------------------
# Make process sleep for t seconds
# Input: time t (seconds)
#        verbose is flag to print system time
# Return: NA
#---------------------------------
def delay(t=0, verbose=False):
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
# Remove special characters from string
'''
Input: input text
Return: input text but with special characters removed
'''
#---------------------------------
def remove_spec_chars(text):
    return re.sub(special_chars, '', text) # regex, replacement str, input text
