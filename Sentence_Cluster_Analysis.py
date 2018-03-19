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

filename = "Master_recipes.txt"

with open(filename, encoding = 'utf-8') as f:
    corpus = f.read()
    


# Let's get the vector coordinates for each step.
# Load the spacy NLP statistical models
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
#pca = PCA(n_components=3)
#pca.fit(X_sents)
#sents2 = pca.transform(X_sents)
#fig = plt.figure(1, figsize=(4, 3))
#plt.clf()
#ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
#ax.scatter(sents2[:,0],sents2[:,1],sents2[:,2], alpha=0.5, c=clusters, cmap=plt.cm.spectral,
 #          edgecolor='k')
 
 #### Build a bigram model #####
model = defaultdict(lambda: defaultdict(lambda:0))

for sentence in sents:
    for w1, w2, w3 in trigrams(sentence, pad_right = True, pad_left = True):
        model[(w1, w2)][w3] += 1
        
# Transform counts to probabilities
for w1_w2 in model:
    total_count = float(sum(model[w1_w2].values()))
    for w3 in model[w1_w2]:
        model[w1_w2][w3] /= total_count
        
## Now generate random text
#import random
#text = [None, None]
#sentence_finished = False
#
#while not sentence_finished:
#    r = random.random()
#    accumulator = .0
#    
#    for word in model[tuple(text[-2:])].keys():
#        accumulator += model[tuple(text[-2:])][word]
#        
#        if accumulator >= r:
#            text.append(word)
#            break
#        
#    if text[-2:] == [None, None]:
#        sentence_finished = True
#
#print(' '.join([t for t in text if t]))