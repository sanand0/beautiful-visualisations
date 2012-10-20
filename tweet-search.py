"""
Pulls all recent UK tweets and prints it

Usage:
    search.py place:6416b8512febefc9    # Search UK tweets
    search.py place:b850c1bfd38f30e0    # Search India tweets
"""

import sys
import urllib
import json
import httplib2

h = httplib2.Http(".cache")

BASE = 'http://search.twitter.com/search.json'
url = BASE + '?result_type=recent&rpp=100&q=%s' % urllib.quote(sys.argv[1])
results = []
while True:
    sys.stderr.write(url + '\n')
    resp, content = h.request(url)
    if resp.status != 200:
        sys.stderr.write(repr(resp) + '\n' + repr(content) + '\n')
        break
    data = json.loads(content)
    results += data['results']

    if 'next_page' in data:
        url = BASE + data['next_page']
    else:
        break

print json.dumps(results)
