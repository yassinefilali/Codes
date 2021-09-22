"""
Graph Mining - ALTEGRAD - Dec 2020
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


############## Task 1
p=r"C:\Users\Yassine\Desktop\ALTEGRAD\lab4\code\datasets\CA-HepTh.txt"
G = nx.read_edgelist(p,delimiter='\t')
print(G.number_of_nodes())
print(G.number_of_edges())



############## Task 2

gcc_nodes=max(nx.connected_components(G))
gcc = G.subgraph(gcc_nodes)
print(gcc.number_of_nodes())
print(gcc.number_of_edges())



############## Task 3
# Degree
degree_sequence = [G.degree(node) for node in G.nodes()]
min_degree=np.min(degree_sequence)
max_degree=np.max(degree_sequence)
mean_degree=np.mean(degree_sequence)
median_degree=np.median(degree_sequence)


############## Task 4

deg=nx.degree_histogram(G)
plt.plot(deg)
plt.xlabel('degree')
plt.ylabel('frequency')
plt.show()




############## Task 5

print('global clustering coefficent : ', nx.transitivity(G))