# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 16:18:56 2018

@author: andro
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 15:19:56 2017

@author: andro
"""

import en_core_web_lg
import numpy as np
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv
from collections import Counter, defaultdict
from nltk import bigrams, trigrams

filename = "./Aggregated_Data/4_All_Directions.txt"

with open(filename, encoding = 'utf-8') as f:
    corpus = f.read()
    

# Some cleaning- get rid of indices before instructions
corpus = corpus.replace("1.", "")
corpus = corpus.replace("2.", "")
corpus = corpus.replace("3.", "")
corpus = corpus.replace("4.", "")
corpus = corpus.replace("5.", "")
corpus = corpus.replace("6.", "")
corpus = corpus.replace("1-", "")
corpus = corpus.replace("2-", "")
corpus = corpus.replace("3-", "")
corpus = corpus.replace("4-", "")
corpus = corpus.replace("5-", "")
corpus = corpus.replace("6-", "")


# Let's get the vector coordinates for each step.
# Load the spacy NLP statistical models
nlp = en_core_web_lg.load()
doc = nlp(corpus)
#chunks = list(doc.noun_chunks)
sents = list(doc.sents)

# Remove any sentences that are just an indexing number (e.g. "3.") or bad parses
for s in sents:
    if len(s) < 3:
        sents.remove(s)


# Initialize a vector storage space 
X_sents = np.zeros((len(sents), 300))

# Get the embeddings for each step
index = 0
for sent in sents:
    X_sents[index,:] = sent.vector
    index= index+1
    
# Do k-means clustering
kmeans = KMeans(n_clusters = 7, random_state = 1).fit(X_sents)
clusters = kmeans.labels_
centers = kmeans.cluster_centers_


# For each cluster center, get the closest element
step_nbrs = NearestNeighbors(n_neighbors=5, algorithm='ball_tree').fit(X_sents)

# Return the index and distance of the closest neighbor
for center in centers:
    new_vec = center.reshape(1,-1)
    distances, indices = step_nbrs.kneighbors(new_vec)
    print(sents[indices[0][0]])
    print(sents[indices[0][1]])
    print(sents[indices[0][2]])
    print(sents[indices[0][3]])
    print(sents[indices[0][4]])
    print('-----------------Next---------------------')
    

    
# Do a PCA analysis to reduce dimensionality for plotting
pca = PCA(n_components=2)
pca.fit(X_sents)
sents2 = pca.transform(X_sents)

# Print to file
with open('./Average/Sentence_PCA.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    fieldnames=['Sentence','Cluster','Coord1','Coord2']
    writer.writerow(fieldnames)
for i in range(0,len(sents)):
    text = sents[i]
    cluster = clusters[i]
    coord1 = sents2[i][0]
    coord2 = sents2[i][1]
    with open('./Average/Sentence_PCA.csv','a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([text] + [cluster] + [coord1] + [coord2])
# Print the PCA components for each sentence as well as the cluster it belongs to. 
#fig = plt.figure(1, figsize=(4, 3))
#plt.clf()
#ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
#ax.scatter(sents2[:,0],sents2[:,1],sents2[:,2], alpha=0.5, c=clusters, cmap=plt.cm.spectral,
 #          edgecolor='k')
 
