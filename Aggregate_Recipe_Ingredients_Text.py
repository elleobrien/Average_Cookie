# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 11:19:14 2018

@author: andro
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 16:41:09 2018

This script puts all the recipes we're going to use in the text analysis into
one document. Then we can feed them into a neural network or a markov analysis.


@author: eobrien
"""
import csv
import pandas as pd

is_conservative = 1
if is_conservative:
    use_row = 3
else:
    use_row = 2
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

# Load in the recipe instructions
for i in index_list:
    # And load in the serving sizes
    filename2 = './Scraped_Recipes/Scrape_Results_AllRecipes/recipe_' + str(i+1) + '.txt'
    with open(filename2) as f:
        text = f.read()
        recipeAR.append(text.strip())
        
# Load in the scaled ingredient lists
ingredient_list_AR = []
# Read in dataframe with pandas
df = pd.read_csv('./Aggregated_Data/0_ingredient_measures_AllRecipes.csv', encoding='latin1')

# Make a list of lists
for i in index_list:
    # Find all the ingredients with this recipe number
     ingredient_df = df.loc[df['Recipe_Index'] == i+1]
     # Get just the ingredients
     ingredients = ingredient_df['Text'].values.tolist()
     ingredient_list_AR.append(ingredients)
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

# Load in the recipe
for i in index_list:
    # And load in the serving sizes
    filename2 = './Scraped_Recipes/Scrape_Results_Epicurious/chocolate+chip+cookies/recipe_' + str(i+1) + '.txt'
    with open(filename2) as f:
        text = f.read()
        recipeEP.append(text.strip())  

# Load in the scaled ingredient lists
ingredient_list_EP = []
# Read in dataframe with pandas
df = pd.read_csv('./Aggregated_Data/0_ingredient_measures_Epicurious.csv', encoding='latin1')

# Make a list of lists
for i in index_list:
    # Find all the ingredients with this recipe number
     ingredient_df = df.loc[df['Recipe_Index'] == i+1]
     # Get just the ingredients
     ingredients = ingredient_df['Text'].values.tolist()
     ingredient_list_EP.append(ingredients)
###############################################################################
# Now get the miscellaneous recipes
###############################################################################
recipeM = []
use_index = []

# Read in the recipe directory, where the recipe index and the boolean "Include this recipe" are listed
# Load in the serving sizes 
index_list = list(range(0,114))
for i in index_list:
    # And load in the serving sizes
    filename2 = './Scraped_Recipes/Scrape_Results_Misc/recipe_' + str(i+1) + '.txt'
    with open(filename2, encoding = 'utf-8',errors='ignore') as f:
        text = f.read()
        recipeM.append(text.strip())  
        
        
# Load in the scaled ingredient lists
ingredient_list_M = []
# Read in dataframe with pandas
df = pd.read_csv('./Aggregated_Data/0_ingredient_measures_Misc.csv', encoding='latin1')

# Make a list of lists
for i in index_list:
    # Find all the ingredients with this recipe number
     ingredient_df = df.loc[df['Recipe_Index'] == i+1]
     # Get just the ingredients
     ingredients = ingredient_df['Text'].values.tolist()
     ingredient_list_M.append(ingredients)



# Concatenate all the lists
master_list = recipeAR + recipeEP + recipeM
master_ing = ingredient_list_AR + ingredient_list_EP + ingredient_list_M

# Write all to a file
newfile = 'Ing_Recipe_Aggregate.txt'
f = open(newfile, 'wb')
for i in range(0,len(master_list)):
    
    ing_list = master_ing[i]
    for item in ing_list:
        if type(item) == str:
            f.write(item.encode('ascii', errors = 'ignore'))
            f.write(b'\n')
    f.write(b'BREAK\n')
    f.write(b'\n\n')
    dir_list = master_list[i]
    f.write(dir_list.encode('ascii',errors = 'ignore'))
    f.write(b'BREAK\n')
    f.write(b'\n\n')

f.close()