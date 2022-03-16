import matplotlib.pyplot as plt
from igraph import *
"""
Task 1. Reproduce the following graph seen in class, that is,
plot the clustering coecient and the average shortestpath
as a function of the parameter p of the Watts-Strogatz model.
"""

def generatePlot(x1, y1, x2, y2, path):
    plt.plot(P,C,'s',P,L,'o')
    plt.xscale('log')
    plt.xlabel('p')
    plt.savefig(path, bbox_inches='tight')

graph = Graph.Watts_Strogatz(1, 1000, 4, 0)
L = []
C = []
#average shortest path
L0 = graph.average_path_length(unconn=True)
#clustering coefficient
C0 = graph.transitivity_undirected()

nData = 14
P = []
value = 0
for x in range(0, nData+1):
    P.insert(0,10**(-value))
    value += 4/nData

for i in range(0, nData+1):
    graph = Graph.Watts_Strogatz(1, 1000, 4, P[i])
    L.append(graph.average_path_length(unconn=True)/L0)
    C.append(graph.transitivity_undirected()/C0) #normalizado

generatePlot(P,C,P,L,'output/ex1.png')
