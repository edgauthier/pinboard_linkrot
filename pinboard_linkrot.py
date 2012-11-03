#!/usr/bin/env python

from __future__ import division
import requests
import json
import sys
from requests.exceptions import SSLError, InvalidSchema, ConnectionError

def get_link_status_code(link):
    headers = {'User-agent':'Mozilla/5.0'}
    try:
        r = requests.head(link, headers=headers, allow_redirects=True)
        return r.status_code
    except (Exception) as e:
        return '%s: %s' % (type(e).__name__, str(e)) 

def is_valid_link(status_code):
    if status_code == 200:
        return True
    else:
        return False 
    
def process_links(links):
    bad_links = 0
    try:
        for link in links:
            status_code = get_link_status_code(link['href'])
            if not is_valid_link(status_code):
                print 'Invalid link (%s): %s [%s]' % (status_code, link['description'], link['href'])
                bad_links += 1
    except KeyboardInterrupt:
        pass
    
    linkrot = int(bad_links/len(links)*100)
    print '\n%s%% linkrot\n' % linkrot
        
def process_bookmarks_file(filename):
    with open(filename) as f:
        bookmarks = json.load(f)
        process_links(bookmarks)
        
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: pinboard_linkrot.py <bookmarks.json>'
        exit(1)
    process_bookmarks_file(sys.argv[1])
