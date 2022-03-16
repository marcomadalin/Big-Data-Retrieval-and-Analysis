import matplotlib.pyplot as plt
from igraph import *


graph = Graph.Read_Edgelist("edges.txt", directed = False)

diameter = graph.get_diameter()
trans = graph.transitivity_undirected()
degreeDis= graph.degree_distribution()
grau = graph.degree()
betweeness = graph.edge_betweenness()

f = open("output/graphRpt.txt", "a")
f.write('Obtained graph:\n')
f.write(str(graph) +  '\n')
f.close()
f = open("output/graphData.txt", "a")
f.write("#Vertexs: " + str(len(graph.es)) + "\n")
f.write("#Edges: " + str(len(graph.vs)) + "\n")
f.write("Diameter: " + str(diameter) + "\n")
f.write("Transitivity: " + str(trans) + "\n")
f.write("Vertex degree: " + str(grau) + "\n")
f.write("Degree distribution: " + str(degreeDis)+ "\n")
f.write("Edge betweeness: " + str(betweeness) + "\n")
f.close()

pageRank = graph.pagerank()
plotPR = plot(graph,vertex_size = [pageRank[i]*500 for i in range(0,len(graph.vs))], target="./output/prGraph.png")

community = Graph.Erdos_Renyi(20,0.3)
plotC = plot(community, layout = community.layout_kamada_kawai(), target="./output/communityGraph.png");
#algoritme de betweeness
C = community.community_edge_betweenness()
cluster = C.as_clustering()
size = cluster.sizes()

#histograma
plt.hist(size, bins=range(min(size),max(size) + 2, 1), align='left')
plt.ylabel('Communities number')
plt.xlabel('Size')
plt.savefig('output/ist_communities.png')

#grafo
comPlt = plot(C.as_clustering(), layout = community.layout_kamada_kawai(),target="./output/clustersGraph.png")
