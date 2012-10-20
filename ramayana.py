"""
Scrapes Ramayana in unicode from http://www.sacred-texts.com/hin/rys/index.htm
"""

import re
import csv
import urllib
import urlparse
import lxml.html
import collections

scrape = lambda url: lxml.html.parse(urllib.urlopen(url))
links = lambda url, r: [a for a in scrape(url).findall('.//a') if r.search(a.get('href'))]

words = collections.Counter()
base = 'http://www.sacred-texts.com/hin/rys/index.htm'
for book in links(base, re.compile(r'rysi\d+')):
    url = urlparse.urljoin(base, book.get('href'))
    for chapter in links(url, re.compile(r'rys\d+')):
        url = urlparse.urljoin(base, chapter.get('href'))
        print url
        tree = scrape(url)
        sanskrit = tree.findall('.//td')[1]
        for line_numbers in sanskrit.findall('font'):
            sanskrit.remove(line_numbers)
        for word in sanskrit.text_content().split():
            words[word] += 1

out = csv.writer(open('ramayana.csv', 'w'), lineterminator='\n')
out.writerow(['word', 'count'])
for word, count in words.most_common():
    out.writerow([word.encode('utf8'), count])
