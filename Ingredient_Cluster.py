#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 15:37:00 2018

Read in all the ingredients and sort them into clusters
@author: eobrien
"""

import en_core_web_lg
import numpy as np
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

filename = "Ing_only.txt"

with open(filename, encoding = 'utf-8') as f:
    corpus = f.read()

corpus = corpus.replace("BREAK", "")
corpus = corpus.replace('\n','. ')

nlp = en_core_web_lg.load()
doc = nlp(corpus)
#chunks = list(doc.noun_chunks)
sents = list(doc.sents)

# Initialize a vector storage space 
X_sents = np.zeros((len(sents), 300))

# Get the embeddings for each step
index = 0
for sent in sents:
    X_sents[index,:] = sent.vector
    index= index+1
    
#### Cluster each ingredient #####
# Do k-means clustering
kmeans = KMeans(n_clusters = 20, random_state = 1).fit(X_sents)
clusters = kmeans.labels_
centers = kmeans.cluster_centers_    
    
# Get the center of each cluster
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
    


# How many are in the first cluster? List them all
a = np.where(clusters == 5)
newlist = [sents[i] for i in a[0]]
print(newlist)

### PCA Visualization ###
pca = PCA(n_components=3)
pca.fit(X_sents)
sents2 = pca.transform(X_sents)
fig = plt.figure(1, figsize=(4, 3))
plt.clf()
ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
ax.scatter(sents2[:,0],sents2[:,1],sents2[:,2], alpha=0.5, cmap=plt.cm.spectral,
           edgecolor='k')