from __future__ import print_function
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

import argparse

from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from elasticsearch.client import CatClient
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q
import math
import functools
import operator
import argparse

import numpy as np

#tdfidf functions
def search_file_by_path(client, index, path):
    """
    Search for a file using its path

    :param path:
    :return:
    """
    s = Search(using=client, index=index)
    q = Q('match', path=path)  # exact search in the path field
    s = s.query(q)
    result = s.execute()

    lfiles = [r for r in result]
    if len(lfiles) == 0:
        raise NameError(f'File [{path}] not found')
    else:
        return lfiles[0].meta.id
def document_term_vector(client, index, id):
    """
    Returns the term vector of a document and its statistics a two sorted list of pairs (word, count)
    The first one is the frequency of the term in the document, the second one is the number of documents
    that contain the term

    :param client:
    :param index:
    :param id:
    :return:
    """
    termvector = client.termvectors(index=index, id=id, fields=['text'],
                                    positions=False, term_statistics=True)

    file_td = {}
    file_df = {}

    if 'text' in termvector['term_vectors']:
        for t in termvector['term_vectors']['text']['terms']:
            file_td[t] = termvector['term_vectors']['text']['terms'][t]['term_freq']
            file_df[t] = termvector['term_vectors']['text']['terms'][t]['doc_freq']
    return sorted(file_td.items()), sorted(file_df.items())
def toTFIDF(client, index, file_id):
    """
    Returns the term weights of a document

    :param file:
    :return:
    """

    # Get the frequency of the term in the document, and the number of documents
    # that contain the term
    file_tv, file_df = document_term_vector(client, index, file_id)

    max_freq = max([f for _, f in file_tv])

    dcount = doc_count(client, index)

    tfidfw = {}
    for (t, w),(_, df) in zip(file_tv, file_df):
        idf = np.log2(dcount/df)
        tf = w/max_freq
        wf = tf * idf
        #tfidfw.append((t, wf))
        tfidfw[t] = wf
    return normalize(tfidfw)
def normalize(d):
    s = sum(d.values())
    r = np.sqrt(s)
    norm = {t: d.get(t, 0)/r for t in set(d)}
    return norm
def doc_count(client, index):
    """
    Returns the number of documents in an index

    :param client:
    :param index:
    :return:
    """
    return int(CatClient(client).count(index=[index], format='json')[0]['count'])
#Auxiliar functions
def queryTransformation(query):
    D = {}
    for elem in query:
        if '^' in elem:
            k, v = elem.split('^')
            v = float(v)
            D[k] = v
        else:
            k = elem
            v = 1.0
            D[k] = v
    return normalize(D)
def inverseQueryTransformation(D):
    query = []
    for i in D:
        q = i + '^' + str(D[i])
        query.append(q)
    return query


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, help='Index to search')
    parser.add_argument('--k', default=None, type=int, help='number of top documents considered relevant and used for applying Rocchio at each round')
    parser.add_argument('--R', default=None, type=int, help='the maximum number of new terms to be kept in the new query')
    parser.add_argument('--nrounds', default=None, type=int, help='the number of applications of Rocchios rule')
    parser.add_argument('--A', default=None, type=int, help='alpha in Rocchio rule')
    parser.add_argument('--B', default=None, type=int, help='beta in Rocchio rule')
    parser.add_argument('--query', default=None, nargs=argparse.REMAINDER, help='List of words to search')

    args = parser.parse_args()

    index = args.index

    #Rocchio parameters
    R = args.R
    nrounds = args.nrounds
    B = args.B
    A = args.A
    k = args.k

    query = args.query

    #print(query)
    nhits = k

    try:
        client = Elasticsearch()
        s = Search(using=client, index=index)

        if query is not None:
            for i in range(0,nrounds):
                q = Q('query_string',query=query[0])
                for j in range(1, len(query)):
                    q &= Q('query_string',query=query[j])

                s = s.query(q)
                response = s[0:nhits].execute()

                #print("Query inicial:")
                #print(query)

                Dquery = queryTransformation(query)
                docs = {}
                for r in response:
                    tw = toTFIDF(client, index, r.meta.id)
                    docs = {t: docs.get(t, 0) + tw.get(t, 0) for t in set(docs) | set(tw)}

                docs = {t: docs.get(t,0)*B/nhits for t in set(docs)}
                oldQuery = {t: Dquery.get(t,0)*A for t in set(Dquery)}
                newQuery = {}
                newQuery = {t: docs.get(t, 0) + oldQuery.get(t, 0) for t in set(docs) | set(oldQuery)}
                newQuery = sorted(newQuery.items(), key=operator.itemgetter(1), reverse = True)
                newQuery = newQuery[:R]
                Dquery = dict((t, v) for (t, v) in newQuery[:50])
                query = inverseQueryTransformation(normalize(Dquery))
                print('Query round ', i, ' :')
                print(query)
                print()
            print('Query final: ')
            print(query)
            print()

            print('Documents :', len(response))
            """
            for r in response:
                print(f'ID= {r.meta.id} SCORE= {r.meta.score}')
                print(f'PATH= {r.path}')
                print(f'TEXT= {r.text[:50]}')
                print('-----------------------------------------------------------------')
            """

        else:
            print('No query parameters passed')

        #print (f"{response.hits.total['value']} Documents")

    except NotFoundError:
        print(f'Index {index} does not exists')
