"""
.. module:: CountWords

CountWords
*************

:Description: CountWords

    Generates a list with the counts and the words in the 'text' field of the documents in an index

:Authors: bejar


:Version:

:Created on: 04/07/2017 11:58

"""

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from elasticsearch.exceptions import NotFoundError, TransportError

import argparse

__author__ = 'bejar'

def number_in (v):
    return any(char.isdigit() for char in s)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, required=True, help='Index to search')
    parser.add_argument('--alpha', action='store_true', default=False, help='Sort words alphabetically')
    args = parser.parse_args()

    index = args.index

    try:
        client = Elasticsearch(timeout=1000)
        voc = {}
        sc = scan(client, index=index, query={"query" : {"match_all": {}}})
        for s in sc:
            try:
                tv = client.termvectors(index=index, id=s['_id'], fields=['text'])
                if 'text' in tv['term_vectors']:
                    for t in tv['term_vectors']['text']['terms']:
                        if t in voc:
                            voc[t] += tv['term_vectors']['text']['terms'][t]['term_freq']
                        else:
                            voc[t] = tv['term_vectors']['text']['terms'][t]['term_freq']
            except TransportError:
                pass
        lpal = []

        for v in voc:
            if not(v == (int)) and not('.' in v) and not('_' in v) and not number_in(v) and len(v) > 1:
                lpal.append((v.encode("utf-8", "ignore"), voc[v]))

        freq = {}
        for pal, cnt in sorted(lpal, key=lambda x: x[0 if args.alpha else 1]):
            freq[pal] = cnt
        #ordenem per frequencia
        freqOrd = sorted(freq, key=freq.get, reverse=True)
        for v in freqOrd:
            print('%d, %s' % (freq[v], v))
        print('%s Words' % len(lpal))
        sum=0
        for l in freqOrd:
            sum += int(freq[l])
        print('%s Words total' % sum)
    except NotFoundError:
        print('Index %s does not exists' % index)
