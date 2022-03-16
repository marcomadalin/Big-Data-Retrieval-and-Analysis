import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

tamanymostra = 500
a = 1.2 #Change the a parameter here.
#Zipf's law formula
def func(x, b, c):
    return c/(x+b)**a

def freqPlot(f, size, name):
    eje_x = []
    eje_y = []
    i = 0
    for k, v in f.items():
        if i < size:
            eje_x.append(k)
            eje_y.append(v)
        i += 1
    plt.bar(eje_x, eje_y)
    plt.show()
    plt.savefig( './results/'+ name + '.png')

def zipfLinear(numArray,freqArray,fitArray, name):
    plt.plot(numArray, freqArray, 'g-', label='Frequencies')
    plt.plot(numArray, fitArray,'r-',label='Zipf\'s fit')
    plt.legend()
    plt.xlabel('Word rank')
    plt.ylabel('Word frequencies')
    plt.show()
    plt.savefig( './results/'+ name + '.png')

def zipfLogPlot(logNumArray,logFreqArray,logFitArray, name):
    plt.plot(logNumArray, logFreqArray, 'g-', label='Frequencies log')
    plt.plot(logNumArray, logFitArray,'r-',label='Log Zipf\'s fit')
    plt.legend()
    plt.xlabel('Log of word rank')
    plt.ylabel('Log of word frequencies ')
    plt.show()
    plt.savefig( './results/'+ name + '.png')

def zipfTest(xdata,ydata,logxdata,logydata):
    popt, pcov = curve_fit(func,xdata,ydata)
    print('parametres optims Zipf:')
    print('b = %d, c = %d' % (popt[0],popt[1]))
    fitArray = []
    logFitArray = []
    for num in xdata:
        fitArray.append(func(num,*popt))
        logFitArray.append(np.log(func(num,*popt)))

    return logFitArray, fitArray


with open('./results/f1.txt', "r") as f:
    lines = f.readlines()

dict = {}
logFreqArray = []
freqArray = []
tamanymostra = len(lines)-2
i = 1
for l in lines[:-2]:
    if i > tamanymostra: break
    cnt = int(l.split()[0][:-1])
    pal = l.split()[1][2:-1]
    dict[pal] = cnt
    freqArray.append(cnt)
    logFreqArray.append(np.log(cnt))
    i += 1
totalWords = int(lines[len(lines)-1].split()[0])
difWords = int(lines[len(lines)-2].split()[0])
numArray = range(1,tamanymostra+1)
logNumArray = np.log(numArray)

#freqPlot(dict, 10, 'frequencies')
logFitArray, fitArray = zipfTest(numArray,freqArray,logNumArray,logFreqArray)
#zipfLogPlot(logNumArray,logFreqArray,logFitArray, 'logplot'+str(tamanymostra))
zipfLinear(numArray,freqArray,fitArray, 'linearplot'+str(tamanymostra))
