from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from elasticsearch.client import CatClient
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q
import os
import matplotlib.pyplot as plt

import argparse

import numpy as np

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

    tfidfw = []
    for (t, w),(_, df) in zip(file_tv, file_df):
        idf = np.log2(dcount/df)
        tf = w/max_freq
        wf = tf * idf
        tfidfw.append((t, wf))
    return tfidfw

def print_term_weigth_vector(twv):
    """
    Prints the term vector and the correspondig weights
    :param twv:
    :return:
    """
    for tw in twv:
        print(tw)
    pass

def normalize(tw):
    """
    Normalizes the weights in t so that they form a unit-length vector
    It is assumed that not all weights are 0
    :param tw:
    :return:
    """
    sum = 0
    for (_,w) in tw:
        sum += w*w

    sq = np.sqrt(sum)

    normalized = []
    for i in tw:
        normalized.append((i[0],i[1]/sq))

    return normalized

def cosine_similarity(tw1, tw2):
    """
    Computes the cosine similarity between two weight vectors, terms are alphabetically ordered
    :param tw1:
    :param tw2:
    :return:
    """
    #S'aplica el algorisme de fusió del mergesort
    ind1 = 0
    ind2 = 0
    sim = 0
    while ind1 < len(tw1) and ind2 < len(tw2):
        (t1,w1) = tw1[ind1]
        (t2,w2) = tw2[ind2]
        if t1 == t2:
            sim += w1 * w2
            ind1 += 1
            ind2 += 1
        elif t1 <= t2:
            ind1 += 1
        else:
            ind2 += 1

    return sim
    return 0

def doc_count(client, index):
    """
    Returns the number of documents in an index

    :param client:
    :param index:
    :return:
    """
    return int(CatClient(client).count(index=[index], format='json')[0]['count'])

def combinaciones(c, n):
    def potencia(c):
        if len(c) == 0:
            return [[]]
        r = potencia(c[:-1])
        return r + [s + [c[-1]] for s in r]

    return [s for s in potencia(c) if len(s) == n]

def printPlot(x,y):
    plt.figure(figsize=(15,6))
    plt.plot(x, y, "o")
    plt.xlabel('Compared texts')
    plt.ylabel('Average similarity')
    plt.show()
    plt.savefig( './results/'+ 'novelsPlot' + '.png')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, required=False, help='Index to search')
    parser.add_argument('--files', default=None, required=False, nargs=2, help='Paths of the files to compare')
    parser.add_argument('--print', default=False, action='store_true', help='Print TFIDF vectors')

    args = parser.parse_args()


    index = args.index
    path = './mixed'
    files = os.listdir(path)
    #print(files)
    #files = [ 'DickensAChristmasCarol', 'DickensGreatExpectations', 'DickensThePickwickPapers']
    combos = combinaciones(files,2)
    client = Elasticsearch(timeout=1000)
    y = [0.02363,0.02309,0.03491, 0.02315, 0.05162, 0.02133, 0.00236,0.10495]
    x = ['novels', 'onlyDickensNovels', 'Math', 'Religion', 'Mixed', 'MathVSNovel', 'MathVSReligion', 'ReligionVSNovels']
    count = 0
    sum = 0
    """
    for (file1, file2) in combos:
        try:

            # Get the files ids
            file1_id = search_file_by_path(client, index, path+'/'+file1)
            file2_id = search_file_by_path(client, index, path+'/'+file2)

            # Compute the TF-IDF vectors
            file1_tw = toTFIDF(client, index, file1_id)
            file2_tw = toTFIDF(client, index, file2_id)

            if args.print:
                print(f'TFIDF FILE {file1}')
                print_term_weigth_vector(file1_tw)
                print ('---------------------')
                print(f'TFIDF FILE {file2}')
                print_term_weigth_vector(file2_tw)
                print ('---------------------')

            #print(file1, file2)
            #x.append(count)
            sim = cosine_similarity(normalize(file1_tw), normalize(file2_tw))
            sum += sim
            #print(f"Similarity = {sim:3.5f}")
            count += 1

        except NotFoundError:
            print(f'Index {index} does not exists')

    """
    printPlot(x,y)
