#!/usr/bin/env python -u
# Run python in unbuffered mode, to use with tail-like apps

from __future__ import division
import requests
import json
import sys
import codecs
import locale

# use preferred encoding, even when piping output to another program or file
sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)

def get_link_status(url):
    headers = {'User-agent': 'Mozilla/5.0 ()'}
    try:
        r = requests.get(url, headers=headers)
        return r.status_code
    except (Exception) as e:
        return '%s: %s' % (type(e).__name__, str(e)) 

def valid_link(status):
    return (status == requests.codes.ok)
    
def ignored_link(link, ignore_tags):
    ignore_tags = set(ignore_tags)
    link_tags = link['tags'].split(' ')
    return True if ignore_tags.intersection(link_tags) else False 

def linkrot_summary_header(ignore_tags):
    msg = '#Pinboard linkrot results\n\n'
    if len(ignore_tags) > 0:
        msg += '**Ignored tags:** %s\n' % (', '.join(ignore_tags))
    return msg

def linkrot_summary_footer(num_bad_links, num_good_links):
    linkrot = int(num_bad_links/num_good_links*100)
    return '\n%s%% linkrot (%s/%s)\n' % (linkrot, num_bad_links, num_good_links)

def invalid_link_message(status, link):
    return '- Invalid link (%s): [%s](%s)  ' % (status, link['description'], link['href'])

def process_links(links, ignore_tags):
    num_bad_links = 0
    num_links_processed = 0

    print linkrot_summary_header(ignore_tags)

    try:
        for link in links:
            if ignored_link(link, ignore_tags): 
                continue
            status = get_link_status(link['href'])
            if not valid_link(status):
                print invalid_link_message(status, link)
                num_bad_links += 1
            num_links_processed += 1
    except KeyboardInterrupt:
        print "\nProcessing cancelled...\n"
        pass
    
    print linkrot_summary_footer(num_bad_links, num_links_processed)
        
def process_bookmarks_file(filename, ignore_tags = []):
    with open(filename) as f:
        bookmarks = json.load(f)
        process_links(bookmarks, ignore_tags)
        
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: pinboard_linkrot.py <bookmarks.json> [space separated tags to ignore]'
        exit(1)
    process_bookmarks_file(sys.argv[1], sys.argv[2:])
