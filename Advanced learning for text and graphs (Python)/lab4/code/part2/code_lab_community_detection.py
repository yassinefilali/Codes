"""
Graph Mining - ALTEGRAD - Dec 2020
"""

import networkx as nx
import numpy as np
from scipy.sparse.linalg import eigs
from random import randint
from sklearn.cluster import KMeans


############## Task 6
# Perform spectral clustering to partition graph G into k clusters
def spectral_clustering(G, k):
    A = nx.adjacency_matrix(G)
    inv_deg_G = [1/G.degree(node) for node in G.nodes()]
    inv_D = np.diag(inv_deg_G)
    I=np.eye(inv_D.shape[0])
    L=I-inv_D@A
    eig_val,eig_vect=eigs(L,k=k,which='SM')
    model = KMeans(n_clusters=k)
    model.fit(eig_vect.real)
    clustering=dict()
    for i,node in enumerate(G.nodes):
        clustering[node]=model.labels_[i]
        
    
    ##################
    # your code here #
    ##################
    
    return clustering



############## Task 7
k=50
p=r"C:\Users\Yassine\Desktop\ALTEGRAD\lab4\code\datasets\CA-HepTh.txt"
G = nx.read_edgelist(p,delimiter='\t')
largest = max(nx.connected_components(G),key=len)
largest = G.subgraph(largest)
clusters=spectral_clustering(largest,k)
print(clusters)


############## Task 8
# Compute modularity value from graph G based on clustering
def modularity(G, clustering):
    
    m=G.number_of_edges()
    clusters=set(clustering.values())
    modularity=0
    for cluster in clusters:
        nodes_in_cluster=[node for node in G.nodes() if clustering[node] == cluster]
        subG=G.subgraph(nodes_in_cluster)
        lc=subG.number_of_edges()
        dc=0
        for node in nodes_in_cluster:
            dc=dc+G.degree(node)
        modularity=modularity+ lc/m - (dc/(2*m))**2
            
    
    return modularity



############## Task 9
random_cluster=dict()

for node in largest.nodes():
    random_cluster[node]=np.random.randint(0,50)
print(modularity(largest,clusters))
print(modularity(largest,random_cluster))    

    