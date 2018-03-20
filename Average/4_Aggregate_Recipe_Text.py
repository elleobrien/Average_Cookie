#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 16:41:09 2018

This script puts all the recipes we're going to use in the text analysis into
one document. Then we can feed them into a neural network or a markov analysis.


@author: eobrien
"""
import csv


is_conservative = 0
if is_conservative:
    use_row = 2
else:
    use_row = 3
################################################################################
# First, get all the AllRecipes instructions that we're going to use.
################################################################################

recipeAR = []
use_index = []

# Read in the recipe directory, where the recipe index and the boolean "Include this recipe" are listed
with open('./Scraped_Recipes/Scrape_Results_AllRecipes/recipe_directory.txt','r',encoding='utf8') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        use_index.append(row[use_row])

# Get the indices of the recipes that we will use
index_list =  [i for i, j in enumerate(use_index) if j == '1']

# Load in the serving sizes 
for i in index_list:
    # And load in the serving sizes
    filename2 = 'Scraped_Recipes/Scrape_Results_AllRecipes/recipe_' + str(i+1) + '.txt'
    with open(filename2) as f:
        text = f.read()
        recipeAR.append(text.strip())
        
###############################################################################
# Now get the Epicurious Recipes
###############################################################################
recipeEP = []
use_index = []

# Read in the recipe directory, where the recipe index and the boolean "Include this recipe" are listed
with open('./Scraped_Recipes/Scrape_Results_Epicurious/recipe_directory.txt','r',encoding='utf8') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        use_index.append(row[use_row])

# Get the indices of the recipes that we will use
index_list =  [i for i, j in enumerate(use_index) if j == '1']

# Load in the serving sizes 
for i in index_list:
    # And load in the serving sizes
    filename2 = 'Scraped_Recipes/Scrape_Results_Epicurious/chocolate+chip+cookies/recipe_' + str(i+1) + '.txt'
    with open(filename2) as f:
        text = f.read()
        recipeEP.append(text.strip())  

###############################################################################
# Now get the miscellaneous recipes
###############################################################################
recipeM = []
use_index = []

# Read in the recipe directory, where the recipe index and the boolean "Include this recipe" are listed
# Load in the serving sizes 
for i in range(0,116):
    # And load in the serving sizes
    filename2 = './Scraped_Recipes/Scrape_Results_Misc/recipe_' + str(i+1) + '.txt'
    with open(filename2, encoding = 'utf-8',errors='ignore') as f:
        text = f.read()
        recipeM.append(text.strip())  

# Concatenate all the lists
master_list = recipeAR + recipeEP + recipeM

# Write them all to a file
newfile = './Aggregated_Data/4_All_Directions.txt'
f = open(newfile, 'wb')
for item in master_list:
        if type(item) == str:
            f.write(item.encode('ascii', errors = 'ignore'))
            f.write(b'\n')
f.close()