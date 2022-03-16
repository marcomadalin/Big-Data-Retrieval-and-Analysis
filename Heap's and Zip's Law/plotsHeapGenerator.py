import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import argparse

def func(N, k, beta):
    return k*(N**beta)

def heapLinear(numArray, freqArray, fitArray):
    plt.plot(numArray, freqArray, 'g-', label='Values')
    plt.plot(numArray, fitArray,'r-',label='Heaps law')
    plt.legend()
    plt.xlabel('Total of words')
    plt.ylabel('Different words')
    plt.show()
    plt.savefig( './results/'+ 'heapplot' + '.png')

def heapLog(logNumArray,logFreqArray,logFitArray):
    print(logNumArray, logFreqArray, logFitArray)
    plt.plot(logNumArray, logFreqArray, 'g-', label='Values log')
    plt.plot(logNumArray, logFitArray,'r-',label='Heaps law log')
    plt.legend()
    plt.xlabel('Total of words')
    plt.ylabel('Different words')
    plt.show()
    plt.savefig( './results/'+ 'heaplogplot' + '.png')

def heap(dif, total):
     popt, pcov = curve_fit(func, total, dif)
     print('Parametres de Heap:')
     print('k = %d, Beta = %d' % (popt[0],popt[1]))
     fitArray = []
     logFitArray = []
     for num in total:
        fitArray.append(func(num,*popt))
        logFitArray.append(np.log(func(num,*popt)))

     #Choose plot here
     heapLinear(total, dif, fitArray)
     #heapLog(np.log(total), np.log(dif), logFitArray)

totalWords = []
difWords = []
index = ["f1", "f2", "f3", "f4", "f5"]

for i in index:
    with open('./results/'+ i + '.txt', "r") as f:
        lines = f.readlines()
    totalWords.append(int(lines[len(lines)-1].split()[0]))
    difWords.append(int(lines[len(lines)-2].split()[0]))

#print(totalWords, difWords)
heap(difWords, totalWords)
