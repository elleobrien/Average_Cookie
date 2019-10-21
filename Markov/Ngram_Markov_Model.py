
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 14:29:54 2018

This script creates an n-gram language model for the recipes

@author: andro
"""
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter
import string
import numpy as np
import random as random

###############################################################################
##                  MARKOV MODEL TO GENERATE RECIPES                            ##
###############################################################################
filename = "Ing_Recipe_Aggregate.txt"

with open(filename, encoding = 'utf-8') as f:
    corpus = f.read()
    
corpus = corpus.lower()
corpus.replace('\n',';')

# Tokenize each document and get bi-,tri-,four-, and five-grams.
token = word_tokenize(corpus)
bigrams = list(ngrams(token,2))
trigrams = list(ngrams(token,3))
fourgrams = list(ngrams(token,4))
fivegrams= list(ngrams(token,5))

c = Counter(bigrams)
d = Counter(trigrams)
e = Counter(fourgrams)
g = Counter(fivegrams)



####### 2 grams #############
start = '1.0'
for i in range(0,70):
    # Find all elements in the bigram corpus that start
    # with startword
    choices = [i for i, j in enumerate(bigrams) if j[0]==start]
    # Get all the bigrams that occur
    newlist = [bigrams[i] for i in choices]
    # Get the most popular one
    c2 = Counter(newlist)
    # Get the most common n-gram from this model 
    new_word = c2.most_common(1)[0][0][1]

    start = new_word
    print(start)

######################## TRIGRAMS ############################################
start1 = '1.0'
start2 = 'cup'

for i in range(0,70):
    # Find all elements in the bigram corpus that start
    # with startword
    choices = [i for i, j in enumerate(trigrams) if j[0]==start1 and j[1] == start2]
    # Get all the bigrams that occur
    newlist = [trigrams[i] for i in choices]
    # Get the most popular one
    d2 = Counter(newlist)
    # Get the most common n-gram from this model 
    new_word = d2.most_common(1)[0][0][2]

    start1 = start2
    start2 = new_word
    print(start2)
    
###### Four grams ###############
start1 = '1.0'
start2 = 'cup'
start3 = 'butter'

model_text = [start1, start2, start3]
for i in range(0,2000):
    cumsum = []
    gram_choices = []
    # Find all elements in the bigram corpus that start
    # with startword
    choices = [i for i, j in enumerate(fourgrams) if j[0]==start1 and j[1] == start2 and j[2] == start3]
    # Get all the bigrams that occur
    newlist = [fourgrams[i] for i in choices]
    # Get the most popular one
    d2 = Counter(newlist)
    
    # Get the cumulative probabilities of 
    for k,v in d2.items():
        cumsum.append(v)
        gram_choices.append(k)
    cumsum = np.array([x / sum(cumsum) for x in cumsum])
    cumsum = np.cumsum(cumsum)
    # Generate a random number
    r = random.random()
    ind = np.min(np.where(cumsum > r))
    # Get the most common n-gram from this model 
    new_word = gram_choices[ind][3]

    start1 = start2
    start2 = start3
    start3 = new_word
    model_text.append(new_word)

out_str = ' '.join(model_text)
out_str =out_str.replace('break', '\n\n')
# Print to file!
with open('Markov_Model_Out.txt', 'w') as thefile:
    thefile.write(out_str)

