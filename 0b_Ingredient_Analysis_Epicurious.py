#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 14:52:48 2017

@author: eobrien
"""
import glob
import os
import pandas as pd
from collections import Counter
from string import digits, punctuation
import re
import numpy as np
import csv
from fractions import Fraction


####### How many servings per recipe ###########################################
################################################################################
# This is the subfolder in which the scraping results are all stored
folders = ["Results_Epicurious"]

n_ingredients = []
servings = []
recipe_index = []
use_index = []

# Read in the recipe directory, where the recipe index and the boolean "Include this recipe" are listed
with open('./Results_Epicurious/recipe_directory.txt','r',encoding='utf8') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        recipe_index.append(row[0])
        use_index.append(row[3])

# Get the indices of the recipes that we will use
index_list =  [i for i, j in enumerate(use_index) if j == '1']

# Load in the serving sizes 
for i in index_list:
    path = os.getcwd() + "/" +  folders[0] + "/chocolate+chip+cookies"
    # And load in the serving sizes
    filename2 = path + '/servings_' + str(int(recipe_index[i])+1) + '.txt'
    with open(filename2) as f:
        text = f.read()
        servings.append(text.strip())
        

###### How many servings?####
servings_batch = []
# Split by the parentheses
for batch_text in servings:
    # Check if servings is given in dozens or individual units
    if "dozen" in batch_text:
        num = re.findall('\d+', batch_text)
        cookie_num_tmp = int(num[0])*12
    else:
        num = re.findall('\d+',batch_text)
        cookie_num_tmp = int(num[0])
    servings_batch.append(cookie_num_tmp)

# How much do we have to scale each recipe by to make 48 cookies?
serving_size = np.array(servings_batch)
scale_factor = 48./serving_size

############## Read in the ingredients and scale them #############################
#####################################################################################

# Read in the ingredients
mass_text = [] # This is the master ingredient list
ingred_source_vector = []
counter = 0
for i in index_list:
    path = os.getcwd() + '/Results_Epicurious/chocolate+chip+cookies/' 
    filename = path + '/ingredients_' + str(i+1) + '.txt'
    scale = scale_factor[counter]
    if scale < 0:
        scale = 1
    print(scale)
        
    with open(filename) as f:
         text = f.read()
         ngred = text.count('\n')
         n_ingredients.append(ngred)
         ingred_source_vector += [i+1]*ngred
         for line in text.split('\n')[:-1]:
             line = line.strip()
             orig_num = re.findall('(\d+[\/\d. ]*|\d)', line)
             if orig_num:
                 float_num = float(sum(Fraction(s) for s in orig_num[0].split()))
                 scaled_num = float_num * scale
                 line = line.replace(orig_num[0], str(scaled_num) + ' ')
             mass_text.append(line)
    counter = counter + 1
    
# Now, we want to sort the ingredients into umbrella categories.
# For example:
# "Eggs" and "Large Eggs" are the same ingredient  
    
# Make all the text lower case and remove hyphens from words
mass_text = [w.lower() for w in mass_text]
mass_text = [w.replace('-',' ') for w in mass_text]
mass_text = [w.replace('(','') for w in mass_text]
mass_text = [w.replace(')','') for w in mass_text]


# Find out which list items correspond to the following popular ingredients:
is_egg =  [i for i, s in enumerate(mass_text) if "egg" in s]
is_flour = [i for i, s in enumerate(mass_text) if "all purpose flour" in s]
is_butter = [i for i, s in enumerate(mass_text) if ("butter" in s) and ("peanut" not in s)] 
is_sugar = [i for i, s in enumerate(mass_text) if ("sugar" in s) and ("brown" not in s)] 
is_b_sugar = [i for i, s in enumerate(mass_text) if ("brown sugar" in s)] 
is_b_powder = [i for i, s in enumerate(mass_text) if ("baking powder" in s)] 
is_b_soda = [i for i, s in enumerate(mass_text) if "baking soda" in s]
is_vanilla = [i for i, s in enumerate(mass_text) if "vanilla extract" in s]
is_salt = [i for i, s in enumerate(mass_text) if " salt" in s]
is_choc_chip =[i for i, s in enumerate(mass_text) if ("chocolate chips" in s) or ("chocolate" in s and "chip" in s)]
is_oat = [i for i, s in enumerate(mass_text) if ("oat" in s) or ("oatmeal" in s)] 
is_walnut = [i for i, s in enumerate(mass_text) if "walnut" in s]
is_cinn = [i for i, s in enumerate(mass_text) if ("cinnamon" in s)] 
is_choc= [i for i, s in enumerate(mass_text) if ("chocolate" in s) and ("chip" not in s)] 
is_fruit =  [i for i, s in enumerate(mass_text) if ("apricot" in s) or ("cherries" in s) or ("raisin" in s) or ("dates" in s)] 
is_coconut = [i for i, s in enumerate(mass_text) if ("coconut" in s)] 
is_milk =  [i for i, s in enumerate(mass_text) if ("milk" in s)] 
is_water =  [i for i, s in enumerate(mass_text) if ("water" in s)] 
is_cocoa = [i for i, s in enumerate(mass_text) if ("cocoa powder" in s)] 
is_pecan = [i for i, s in enumerate(mass_text) if ("pecan" in s)] 
is_spray = [i for i, s in enumerate(mass_text) if ("spray" in s)] 
is_shortening = [i for i, s in enumerate(mass_text) if ("shortening" in s)] 
is_marg = [i for i, s in enumerate(mass_text) if ("margarine" in s)] 
is_w_flour = [i for i, s in enumerate(mass_text) if ("wheat" in s) and ("flour" in s)] 
is_c_starch = [i for i, s in enumerate(mass_text) if ("corn starch" in s) or ("cornstarch" in s)] 

category_list = is_egg + is_flour + is_butter + is_sugar + is_b_sugar + is_b_soda \
                + is_vanilla + is_salt + is_choc_chip + is_oat + is_walnut + \
                is_cinn + is_choc + is_fruit + is_coconut + is_milk + is_water \
                + is_b_powder + is_cocoa + is_pecan + is_spray + is_shortening \
                + is_marg + is_w_flour + is_c_starch
                
# Get all the numbers that are not categorized
whole_list = [i for i, s in enumerate(mass_text)]
non_categorized = list(set(whole_list) - set(category_list))

# The rest of the ingredients can be labelled by hand
# zip each list to a dictionary
dict1 = dict(zip(is_egg, ['egg']*len(is_egg)))
dict2 = dict(zip(is_flour, ['all purpose flour']*len(is_flour)))
dict3 = dict(zip(is_butter, ['butter']*len(is_butter)))
dict4 = dict(zip(is_b_sugar, ['brown sugar']*len(is_b_sugar)))
dict5 = dict(zip(is_b_powder, ['baking powder']*len(is_b_powder)))
dict6 = dict(zip(is_b_soda, ['baking soda']*len(is_b_soda)))
dict7 = dict(zip(is_vanilla, ['vanilla']*len(is_vanilla)))
dict8 = dict(zip(is_salt, ['salt']*len(is_salt)))
dict9 = dict(zip(is_choc_chip, ['chocolate chip']*len(is_choc_chip)))
dict10 = dict(zip(is_oat, ['oat']*len(is_oat)))
dict11 = dict(zip(is_walnut, ['walnut']*len(is_walnut)))
dict12= dict(zip(is_cinn, ['cinnamon']*len(is_cinn)))
dict13 = dict(zip(is_choc, ['chocolate']*len(is_choc))) 
dict14 =dict(zip(is_fruit, ['fruit']*len(is_fruit)))
dict15 = dict(zip(is_coconut, ['coconut']*len(is_coconut)))
dict16 = dict(zip(is_milk, ['milk']*len(is_milk)))
dict17 = dict(zip(is_water, ['water']*len(is_water)))
dict18 = dict(zip(is_cocoa, ['cocoa']*len(is_cocoa)))
dict19 = dict(zip(is_pecan, ['pecan']*len(is_pecan)))
dict20 = dict(zip(is_spray, ['cooking spray']*len(is_spray)))
dict21 = dict(zip(is_shortening, ['shortening']*len(is_shortening)))
dict22 = dict(zip(is_marg, ['margarine']*len(is_marg)))
dict23 = dict(zip(is_w_flour, ['wheat flour']*len(is_w_flour)))
dict24 = dict(zip(is_c_starch, ['cornstarch']*len(is_c_starch)))
dict25 = dict(zip(non_categorized, ['other']*len(non_categorized)))
dict26 = dict(zip(is_sugar, ['sugar']*len(is_sugar)))
# Merge into one dictionary# Maybe there is a better way to code this?
dict_grand = dict1.copy()
dict_grand.update(dict2)
dict_grand.update(dict3)
dict_grand.update(dict4)
dict_grand.update(dict5)
dict_grand.update(dict6)
dict_grand.update(dict7)
dict_grand.update(dict8)
dict_grand.update(dict9)
dict_grand.update(dict10)
dict_grand.update(dict11)
dict_grand.update(dict12)
dict_grand.update(dict13)
dict_grand.update(dict14)
dict_grand.update(dict15)
dict_grand.update(dict16)
dict_grand.update(dict17)
dict_grand.update(dict18)
dict_grand.update(dict19)
dict_grand.update(dict20)
dict_grand.update(dict21)
dict_grand.update(dict22)
dict_grand.update(dict23)
dict_grand.update(dict24)
dict_grand.update(dict25)
dict_grand.update(dict26)


####### Read in ratings #############
ratings = []
# Load in the rating
for i in range(0,len(index_list)):
    path = os.getcwd() + "/Results_Epicurious/chocolate+chip+cookies/" 
    # And load in the serving sizes
    filename2 = path + '/rating_' + str(index_list[i] + 1) + '.txt'
    with open(filename2) as f:
        line = f.read()
        line = line.strip()
        orig_num = re.findall('(\d+[\/\d. ]*|\d)', line)
        scaled_num = 'NA'
        if orig_num:
            float_num = orig_num[0].split("/")
            scaled_num = float(float_num[0])/float(float_num[1])
        ratings.append(str(scaled_num))
        



# Now print to one .CSV table 
#
# FORMAT:
# Ingredient category, entry, source recipe index 

# Find all occurrences of these ingredients in our consolidated list
with open('ingredient_measures_Epicurious.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    fieldnames=['Ingredient','Text','Recipe_Index','Rating']
    writer.writerow(fieldnames)
for i in whole_list:
    category = dict_grand[i]
    text = mass_text[i]
    recipe_index = ingred_source_vector[i]
    rating = ratings[index_list.index(ingred_source_vector[i]-1)]
    with open('ingredient_measures_Epicurious.csv','a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([category] + [text] + [recipe_index] + [rating])
        
       


