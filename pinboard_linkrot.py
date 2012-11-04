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

def get_link_status_code(link):
    headers = {'User-agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers)
        return r.status_code
    except (Exception) as e:
        return '%s: %s' % (type(e).__name__, str(e)) 

def is_valid_link(status_code):
    return (status_code == 200)
    
def process_links(links, ignore_tags):
    bad_links = 0
    ignore_tags = set(ignore_tags)
    print '#Pinboard linkrot results\n'
    print '**Ignored tags:** %s\n' % (', '.join(ignore_tags))
    try:
        for link in links:
            # If the link includes any of the ignored tags, skip this link
            if len(ignore_tags.intersection(link['tags'].split(' '))) > 0: continue
            status_code = get_link_status_code(link['href'])
            if not is_valid_link(status_code):
                print '- Invalid link (%s): [%s](%s)  ' % (status_code, link['description'], link['href'])
                bad_links += 1
    except KeyboardInterrupt:
        pass
    
    linkrot = int(bad_links/len(links)*100)
    print '\n%s%% linkrot (%s/%s)\n' % (linkrot, bad_links, len(links))
        
def process_bookmarks_file(filename, ignore_tags = []):
    with open(filename) as f:
        bookmarks = json.load(f)
        process_links(bookmarks, ignore_tags)
        
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: pinboard_linkrot.py <bookmarks.json> [space separated tags to ignore]'
        exit(1)
    process_bookmarks_file(sys.argv[1], sys.argv[2:])
