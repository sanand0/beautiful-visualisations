"""
Converts a Twitter JSON file provided by tweets-search.py into a word count file
"""

import re
import sys
import csv
import json
import collections
import nltk.corpus

stopwords = set(nltk.corpus.stopwords.words('english') + ['jsfoo', 'http', 'amp'])
re_word = re.compile(r'[a-z0-9\']+')
words = collections.Counter()
for tweet in json.loads(open(sys.argv[1]).read()):
    for word in re_word.findall(tweet['text'].lower()):
        if len(word) > 2 and word not in stopwords:
            words[word] += 1

out = csv.writer(sys.stdout, lineterminator='\n')
out.writerow(['word', 'count'])
for word, count in words.most_common():
    out.writerow([word.encode('utf8'), count])
