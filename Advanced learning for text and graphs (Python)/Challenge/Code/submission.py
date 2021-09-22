import pandas as pd
import numpy as np
import networkx as nx
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from gensim.models import Word2Vec
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from lightgbm import LGBMRegressor
from sklearn.preprocessing import scale

def random_walk(G, node, walk_length):
    
    walk=[node]
    for i in range(walk_length):
        neighbours = G.neighbors(walk[i])
        next = np.random.choice(list(neighbours))
        walk.append(next)
    
    walk = [str(node) for node in walk]
    return walk

# Runs "num_walks" random walks from each node
def generate_walks(G, num_walks, walk_length):
    walks = []
    nodes=G.nodes()
    for i in range(num_walks):
        
        for n in np.random.permutation(nodes):
            walks.append(random_walk(G,n,walk_length))
        
    return walks

# Simulates walks and uses the Skipgram model to learn node representations
def deepwalk(G, num_walks, walk_length, n_dim):
    print("Generating walks")
    walks = generate_walks(G, num_walks, walk_length)

    print("Training word2vec")
    model = Word2Vec(size=n_dim, window=8, min_count=0, sg=1, workers=8)
    model.build_vocab(walks)
    model.train(walks, total_examples=model.corpus_count, epochs=5)

    return model

'Reading the Training data'
df_train = pd.read_csv('train.csv', dtype={'authorID': np.int64})
n_train = df_train.shape[0]
 
'Reading the Test data'
df_test = pd.read_csv('test.csv', dtype={'authorID': np.int64})
n_test = df_test.shape[0]
'' 
'Read the author embedding from abstracts' 
embeddings = pd.read_csv("mean_sum.csv")
embeddings = embeddings.iloc[:,1:]
embeddings = embeddings.rename(columns={'0': "authorID"}) #(take mean, sum and std)
####### Uncomment below in order to only take mean and sum 
embeddings = embeddings.iloc[:,:1+256*2]

 
'Merging on authorID'
X_train = df_train.merge(embeddings, on="authorID")
y_train = X_train.h_index
X_train  = X_train.iloc[:,2:]
X_test = df_test.merge(embeddings, on="authorID")
X_test  = X_test.iloc[:,2:]
 
'Applying PCA to reduce dimension of the embedding space' 
AUT = pd.concat([X_train,X_test])
P = PCA(n_components=70)
AUT = scale(AUT)
P.fit(AUT)
AUT = P.fit_transform(AUT)
X_train = AUT[:23124]
X_test = AUT[23124:]
 
 
'Reading the Graph'
G = nx.read_edgelist('collaboration_network.edgelist', delimiter=' ', nodetype=int)
n_nodes = G.number_of_nodes()
n_edges = G.number_of_edges() 
print('Number of nodes:', n_nodes)
print('Number of edges:', n_edges)
 
'Compute the core_number for each node'
core_number = nx.core_number(G)

'Compute the average neighbor degree for each node'
avg_neighbor_degree = nx.average_neighbor_degree(G)

'Computing a dictionnary where the keys are the authors and the values are lists of' 
'publications he authored'
f = open("author_papers.txt","r")
papers_set = set()
d = {}
for l in f:
    auth_paps = [paper_id.strip() for paper_id in l.split(":")[1].replace("[","").replace("]","").replace("\n","").replace("\'","").replace("\"","").split(",")]
    d[l.split(":")[0]] = auth_paps
f.close()
##############################################################################
s = []
f = open("author_papers.txt","r")
papers_set = set()
for l in f:
    auth_paps = [paper_id.strip() for paper_id in l.split(":")[1].replace("[","").replace("]","").replace("\n","").replace("\'","").replace("\"","").split(",")]
    for e in auth_paps :
        s.append(e)
f.close()
 
#size = len(s)
##############################################################################
'Computing the number of authors per paper'
dict = {}
for paper in set(s):
    dict[paper] = 0
 
 
for paper in s:
    dict[paper]+=1
##############################################################################
'Computing the betwenness centrality for each node'
# uncomment to execute, might take some time
## centrality = nx.betwenness_centrality(G,k=500)
dd = pd.read_csv('centrality.csv')
keys = list(dd.iloc[0,1:])
values = list(dd.iloc[1,1:])
centrality = {keys[i]:values[i] for i in range(len(keys))}
##############################################################################
'Computing the clustering coefficient for each node'
# uncomment to execute, might take some time
# clustering  = nx.clustering(G) 
dd = pd.read_csv('clustering.csv')
keys = list(dd.iloc[0,1:])
values = list(dd.iloc[1,1:])
clustering = {keys[i]:values[i] for i in range(len(keys))}
##############################################################################
'Computing the PageRank for each node'
pagerank = nx.pagerank(G)
##############################################################################
'Extracting features for each node in the training and test set'
graph_features_train = np.zeros((n_train, 35))
for i,row in df_train.iterrows():
    #print( round(i*100/len(df_train),2),"%" )
 
    node = row['authorID']
    graph_features_train[i,0] = G.degree(node)
    graph_features_train[i,1] = core_number[node]
    graph_features_train[i,2] = avg_neighbor_degree[node]
    graph_features_train[i,3] = len(d[str(int(node))])
    graph_features_train[i,4] = np.sum([dict[e] for e in  d[str(int(node))] ])
    graph_features_train[i,5] = min([G.degree(n) for n in list(G.neighbors(node))])
    graph_features_train[i,6] = max([G.degree(n) for n in list(G.neighbors(node))])
    graph_features_train[i,7] = np.sum([G.degree(n) for n in list(G.neighbors(node))])
    graph_features_train[i,8] = np.std([G.degree(n) for n in list(G.neighbors(node))])
    graph_features_train[i,9] = min([core_number[n] for n in list(G.neighbors(node))])
    graph_features_train[i,10] = max([core_number[n] for n in list(G.neighbors(node))])
    graph_features_train[i,11] = np.sum([core_number[n] for n in list(G.neighbors(node))])
    graph_features_train[i,12] = np.std([core_number[n] for n in list(G.neighbors(node))])
    graph_features_train[i,13] = np.exp(centrality[node])
    graph_features_train[i,14] = min([np.exp(centrality[n]) for n in list(G.neighbors(node)) if n in centrality])
    graph_features_train[i,15] = max([np.exp(centrality[n]) for n in list(G.neighbors(node)) if n in centrality])
    graph_features_train[i,16] = np.sum([np.exp(centrality[n]) for n in list(G.neighbors(node)) if n in centrality])
    graph_features_train[i,17] = np.std([np.exp(centrality[n]) for n in list(G.neighbors(node)) if n in centrality])
    graph_features_train[i,18] = np.mean([np.exp(centrality[n]) for n in list(G.neighbors(node)) if n in centrality])
 
 
    graph_features_train[i,19] = clustering[node]
    graph_features_train[i,20] = min([clustering[n] for n in list(G.neighbors(node)) if n in clustering])
    graph_features_train[i,21] = max([clustering[n] for n in list(G.neighbors(node)) if n in clustering])
    graph_features_train[i,22] = np.sum([clustering[n] for n in list(G.neighbors(node)) if n in clustering])
    graph_features_train[i,23] = np.std([clustering[n] for n in list(G.neighbors(node)) if n in clustering])
    graph_features_train[i,24] = np.mean([clustering[n] for n in list(G.neighbors(node)) if n in clustering])
    graph_features_train[i,25] = np.exp(pagerank[node])
    graph_features_train[i,26] = min([np.exp(pagerank[n]) for n in list(G.neighbors(node)) if n in pagerank])
    graph_features_train[i,27] = max([np.exp(pagerank[n]) for n in list(G.neighbors(node)) if n in pagerank])
    graph_features_train[i,28] = np.sum([np.exp(pagerank[n]) for n in list(G.neighbors(node)) if n in pagerank])
    graph_features_train[i,29] = np.std([np.exp(pagerank[n]) for n in list(G.neighbors(node)) if n in pagerank])
    graph_features_train[i,30] = np.mean([np.exp(pagerank[n]) for n in list(G.neighbors(node)) if n in pagerank])
    graph_features_train[i,31] = np.std([dict[e] for e in  d[str(int(node))] ])
    graph_features_train[i,32] = np.mean([dict[e] for e in  d[str(int(node))] ])
    graph_features_train[i,33] = np.max([dict[e] for e in  d[str(int(node))] ])
    graph_features_train[i,34] = np.min([dict[e] for e in  d[str(int(node))] ])
 
g_features_train = pd.DataFrame(graph_features_train)


#final_features_train = final_features_train.iloc[:,2:]
 
graph_features_test = np.zeros((n_test, 35))
for i,row in df_test.iterrows():
    #print( round(i*100/len(df_test),2),"%" )
    node = row['authorID']
    graph_features_test[i,0] = G.degree(node)
    graph_features_test[i,1] = core_number[node]
    graph_features_test[i,2] = avg_neighbor_degree[node]
    graph_features_test[i,3] = len(d[str(int(node))])
    graph_features_test[i,4] = np.sum([dict[e] for e in  d[str(int(node))] ])
    graph_features_test[i,5] = min([G.degree(n) for n in list(G.neighbors(node))])
    graph_features_test[i,6] = max([G.degree(n) for n in list(G.neighbors(node))])
    graph_features_test[i,7] = np.sum([G.degree(n) for n in list(G.neighbors(node))])
    graph_features_test[i,8] = np.std([G.degree(n) for n in list(G.neighbors(node))])
    graph_features_test[i,9] = min([core_number[n] for n in list(G.neighbors(node))])
    graph_features_test[i,10] = max([core_number[n] for n in list(G.neighbors(node))])
    graph_features_test[i,11] = np.sum([core_number[n] for n in list(G.neighbors(node))])
    graph_features_test[i,12] = np.std([core_number[n] for n in list(G.neighbors(node))])
 
    graph_features_test[i,13] = np.exp(centrality[node])
    graph_features_test[i,14] = min([np.exp(centrality[n]) for n in list(G.neighbors(node)) if n in centrality])
    graph_features_test[i,15] = max([np.exp(centrality[n]) for n in list(G.neighbors(node)) if n in centrality])
    graph_features_test[i,16] = np.sum([np.exp(centrality[n]) for n in list(G.neighbors(node)) if n in centrality])
    graph_features_test[i,17] = np.std([np.exp(centrality[n]) for n in list(G.neighbors(node)) if n in centrality])
    graph_features_test[i,18] = np.mean([np.exp(centrality[n]) for n in list(G.neighbors(node)) if n in centrality])
 
 
    graph_features_test[i,19] = clustering[node]
    graph_features_test[i,20] = min([clustering[n] for n in list(G.neighbors(node)) if n in clustering])
    graph_features_test[i,21] = max([clustering[n] for n in list(G.neighbors(node)) if n in clustering])
    graph_features_test[i,22] = np.sum([clustering[n] for n in list(G.neighbors(node)) if n in clustering])
    graph_features_test[i,23] = np.std([clustering[n] for n in list(G.neighbors(node)) if n in clustering])
    graph_features_test[i,24] = np.mean([clustering[n] for n in list(G.neighbors(node)) if n in clustering])
    graph_features_test[i,25] = np.exp(pagerank[node])
    graph_features_test[i,26] = min([np.exp(pagerank[n]) for n in list(G.neighbors(node)) if n in pagerank])
    graph_features_test[i,27] = max([np.exp(pagerank[n]) for n in list(G.neighbors(node)) if n in pagerank])
    graph_features_test[i,28] = np.sum([np.exp(pagerank[n]) for n in list(G.neighbors(node)) if n in pagerank])
    graph_features_test[i,29] = np.std([np.exp(pagerank[n]) for n in list(G.neighbors(node)) if n in pagerank])
    graph_features_test[i,30] = np.mean([np.exp(pagerank[n]) for n in list(G.neighbors(node)) if n in pagerank])
    graph_features_test[i,31] = np.std([dict[e] for e in  d[str(int(node))] ])
    graph_features_test[i,32] = np.mean([dict[e] for e in  d[str(int(node))] ])
    graph_features_test[i,33] = np.max([dict[e] for e in  d[str(int(node))] ])
    graph_features_test[i,34] = np.min([dict[e] for e in  d[str(int(node))] ])
g_features_test = pd.DataFrame(graph_features_test)


##################################################
'Unsupervised Feature Exctraction for test data'
'Different unsupervised models'
# P = GGVec(n_component = 100)
# P = ProNE(n_component = 100)
# P = Node2Vec(n_component = 100)
# emb = P.fit_transform(G)
'DeepWalk'
# n_dim = 100
# n_walks = 100
# walk_length = 10
# model = deepwalk(G, n_walks, walk_length, n_dim)
# emb = np.zeros((n_nodes, n_dim))
# for i, node in enumerate(G.nodes()):
#     emb[i,:] = model.wv[str(node)]
'Getting features for respective nodes'
# N = G.nodes()
# g_emb_test = pd.DataFrame(emb)
# g_emb_test['nodes'] = list(N)
# test_nodes = list(df_test.authorID)
# g_emb_test = g_emb_test[g_emb_test.nodes.isin(test_nodes)].iloc[:,:g_emb_test.shape[1]-1]
# g_emb_test = g_emb_test.reset_index(drop=True)
##################################################
##################################################
'Unsupervised Feature Exctraction for train data'
# N = G.nodes()
# g_emb_train = pd.DataFrame(emb)
# g_emb_train['nodes'] = list(N)
# train_nodes = list(df_train.authorID)
# g_emb_train = g_emb_train[g_emb_train.nodes.isin(train_nodes)].iloc[:,:g_emb_train.shape[1]-1]
# g_emb_train = g_emb_train.reset_index(drop=True)
##################################################
'Concating text and graph features'


final_features_test = pd.concat([pd.DataFrame(X_test),g_features_test],axis=1)
final_features_train = pd.concat([pd.DataFrame(X_train),g_features_train],axis=1)
##### Uncomment if using unsupervised graph embedding
# final_features_test = pd.concat([pd.DataFrame(X_test),g_features_test,g_emb_test],axis=1)
# final_features_train = pd.concat([pd.DataFrame(X_train),g_features_train,g_emb_train],axis=1)

final_features_train.columns = [str(i) for i in range(final_features_train.shape[1])]
 
final_features_test.columns = [str(i) for i in range(final_features_test.shape[1])]

'Testing different models'
#reg = RandomForestRegressor(n_estimators=100, criterion="mae", max_depth=10)
reg = LGBMRegressor(n_estimators = 15000, subsample = 0.7,max_depth=14, 
                    colsample_bytree=0.8, learning_rate=0.01,n_jobs=-1
                    ,random_state=0,bagging_freq= 5, bagging_fraction= 0.75
                    ,reg_sqrt=True)
#reg = XGBRegressor(n_estimators=10000 , max_depth=8,subsample=0.7, learning_rate=0.01,colsample_bytree=0.7,min_child_weight=5,random_state=0)
print("fitting")
reg.fit(final_features_train, y_train)
print("predicting")
y_pred = reg.predict(final_features_test).astype(int)

 
'Write the predictions to the test csv file'
df_test['h_index_pred'].update(pd.Series(np.round_(y_pred, decimals=3)))
df_test.loc[:,["authorID","h_index_pred"]].to_csv('test_predictions.csv', index=False)