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



###############################################################################
##                  RECIPE ANALYSIS                                          ##
###############################################################################
filename = "Master_recipes.txt"

with open(filename, encoding = 'utf-8') as f:
    corpus = f.read()
    
corpus = corpus.lower()

token = word_tokenize(corpus)
bigrams = list(ngrams(token,2))
trigrams = list(ngrams(token,3))
fourgrams = list(ngrams(token,4))

c = Counter(bigrams)
d = Counter(trigrams)
e = Counter(fourgrams)

start = 'bake'

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
start1 = 'preheat'
start2 = 'oven'

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
    
################################## Four grams ################################
start1 = 'preheat'
start2 = 'oven'
start3 = 'to'

for i in range(0,80):
    # Find all elements in the bigram corpus that start
    # with startword
    choices = [i for i, j in enumerate(fourgrams) if j[0]==start1 and j[1] == start2 and j[2] == start3]
    # Get all the bigrams that occur
    newlist = [fourgrams[i] for i in choices]
    # Get the most popular one
    d2 = Counter(newlist)
    # Get the most common n-gram from this model 
    new_word = d2.most_common(1)[0][0][3]

    start1 = start2
    start2 = start3
    start3 = new_word
    print(start3)
    
###############################################################################
##               INGREDIENT ANALYSIS                                         ##
###############################################################################