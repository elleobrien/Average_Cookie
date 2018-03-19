# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 21:21:00 2018

@author: andro
"""

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

###############################################################################
##                  RECIPE ANALYSIS                                          ##
###############################################################################
filename = "Ing_only.txt"

with open(filename, encoding = 'utf-8') as f:
    corpus = f.read()
    
corpus = corpus.lower()
corpus.replace('\n',';')

# Get the first three words of each document


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
for i in range(0,250):
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
    
    
###### Five grams #########
    ###### Four grams ###############
start1 = '2.0'
start2 = 'teaspoon'
start3 = 'baking'
start4 = 'soda'

model_text = [start1,start2,start3,start4]
for i in range(0,200):
    # Find all elements in the bigram corpus that start
    # with startword
    cumsum = [];
    gram_choices = [];
    choices = [i for i, j in enumerate(fivegrams) if j[0]==start1 and j[1] == start2 and j[2] == start3
               and start4 == j[3]]
    # Get all the bigrams that occur
    newlist = [fivegrams[i] for i in choices]
    # Get the most popular one
    e2 = Counter(newlist)
    # Get the most common n-gram from this model 
        # Get the cumulative probabilities of 
    for k,v in e2.items():
        cumsum.append(v)
        gram_choices.append(k)
    cumsum = np.array([x / sum(cumsum) for x in cumsum])
    cumsum = np.cumsum(cumsum)
    # Generate a random number
    r = random.random()
    ind = np.min(np.where(cumsum > r))
    # Get the most common n-gram from this model 
    new_word = gram_choices[ind][4]

    start1 = start2
    start2 = start3
    start3 = start4
    start4 = new_word
    model_text.append(new_word)


























def is_number(n):
    try:
        float(n)   # Type-casting the string to `float`.
                   # If string is not a valid `float`, 
                   # it'll raise `ValueError` exception
    except ValueError:
        return False
    return True    
################################## Four grams ################################
ingredient_list = ["butter","flour","eggs","baking",
                   "chocolate","walnuts","brown","sugar",
                   "vanilla","salt"]


for item in ingredient_list:
    # Find all elements in the bigram corpus that start
    # with startword
    choices = [i for i, j in enumerate(fourgrams) if j[0]==item or j[1] == item or j[2] == item]
    # Get all the bigrams that occur
    newlist = [fourgrams[i] for i in choices]
    # Get the most popular one
    d2 = Counter(newlist)
    # Go down the list until a number appears in the n-gram
    fetch = 1
    has_num = 0
    while has_num == 0:
        check = d2.most_common(fetch)
        if is_number(check[fetch-1][0][0]):
            start_gram = check[fetch-1]
            has_num = 1
        fetch = fetch+1
    print(start_gram)


###############################################################################
##               INGREDIENT ANALYSIS                                         ##
###############################################################################