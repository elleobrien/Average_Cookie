#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 14:52:48 2017

@author: eobrien
"""
import glob
import os
import pandas as pd
from collections import Counter
from string import digits
import re
import numpy as np
import csv
from fractions import Fraction


folders = ["chocolate+chip+cookies"]

mass_text = []
n_ingredients = []
servings = []

recipe_index = []
use_index = []
with open(os.getcwd() + '\\Results\\'+ folders[0] + '\\recipe_directory.txt','r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        recipe_index.append(row[0])
        use_index.append(row[2])

index_list =  [i for i, j in enumerate(use_index) if j == '1']

for i in index_list:
    path = os.getcwd() + '/Results/' + folders[0]
    filename = path + '/ingredients_' + str(i+1) + '.txt'
    with open(filename) as f:
         text = f.read()
         mass_text.extend(text.split('\n')[:-1])
         n_ingredients.append(text.count('\n'))
    filename2 = path + '/servings_' + str(i+1) + '.txt'
    with open(filename2) as f:
        text = f.read()
        servings.append(text.strip())
        

###### How many servings?####
servings_batch = []
# Split by the parentheses
for s in servings:
    batch_text = s[s.find("(")+1:s.find(")")]
    if "dozen" in batch_text:
        num = re.findall('\d+', batch_text)
        cookie_num_tmp = int(num[0])*12
    elif "cookies" in batch_text:
        num = re.findall('\d+',batch_text)
        cookie_num_tmp = int(num[0])
    else: 
        cookie_num_tmp = -1 # Flag for didn't get it
    servings_batch.append(cookie_num_tmp)

# How many cookies are in the average recipe serving size?
serving_size = np.array(servings_batch)
mean_cookies = np.mean(serving_size[serving_size > 0])

scale_factor = 48./serving_size

float(sum(Fraction(s) for s in '1 2/3'.split()))
# Now we need to go back and scale all the ingredient numbers
mass_text = []
counter = 0
for i in index_list:
    path = os.getcwd() + '/Results/' + folders[0]
    filename = path + '/ingredients_' + str(i+1) + '.txt'
    scale = scale_factor[counter]
    if scale < 0:
        scale = 1
    print(scale)
        
    with open(filename) as f:
         text = f.read()
         n_ingredients.append(text.count('\n'))
         for line in text.split('\n')[:-1]:
             line = line.strip()
             orig_num = re.findall('(\d+[\/\d. ]*|\d)', line)
             if orig_num:
                 float_num = float(sum(Fraction(s) for s in orig_num[0].split()))
                 scaled_num = float_num * scale
                 line = line.replace(orig_num[0], str(scaled_num) + ' ')
             mass_text.append(line)
    counter = counter + 1
         





    

remove_digits = str.maketrans('', '', digits)
clean_list = []
# Remove digits and units of measure from each line
for item in mass_text:
    item = item.lower()
    no_digit = item.translate(remove_digits)
    out = no_digit.replace('tablespoons', '')
    out = out.replace('tablespoon', '')
    out = out.replace('teaspoons', '')
    out = out.replace('teaspoon', '')
    out = out.replace('cups', '')
    out = out.replace('cup', '')
    out = out.replace('ounces', '')
    out = out.replace('ounce', '')
    out = out.replace('pounds', '')
    out = out.replace('pound', '')
    out = out.replace('handfuls', '')
    out = out.replace('handful', '')
    out = out.replace('packages', '')
    out = out.replace('package', '')
    out = out.replace('bags', '')
    out = out.replace('bag', '')
    out = out.replace('/', '')
    out = re.sub("[\(\[].*?[\)\]]", "", out) # remove bracketed descriptors
    out, sep, tail = out.partition(',') # remove anything that comes after a comma
    
    #if out != '':
    clean_list.append(out.strip())

# How many ingredients does the average cookie have?
avg_ingredients_count = int(round(numpy.mean(n_ingredients)))

 # Now make counts of the occurrences of strings
tally= Counter(clean_list)
tally.most_common(50)
    
# Based on what we're seeing in the top fifty ingredients, a few consolidations
consolidated_list = []
for item in clean_list:
    item = item.replace('. ','')
    out = item.replace('packed', '')
    out = out.replace('semisweet chocolate chips', 'chocolate chips')
    out = out.replace('semi-sweet chocolate chips', 'chocolate chips')
    out = out.replace('large egg', 'egg')
    out = out.replace('eggs', 'egg')
    out = out.replace('vegetable shortening', 'shortening')
    out = out.replace('butter flavored shortening', 'shortening')
    out = out.replace('chopped', '')
    out = out.replace('white sugar', 'sugar')
    out = out.replace('unsalted butter','butter')
    out = out.replace('salted butter','butter')
    out = out.replace('light brown sugar','brown sugar')
    consolidated_list.append(out.strip())
    
tally2 = Counter(consolidated_list)
tally2.most_common(avg_ingredients_count)

# Print to a csv#lets say you stored the counter in a variable called cnter
with open('ingredient_tally.csv','w') as csvfile:
    fieldnames=['ingredient','count']
    writer=csv.writer(csvfile)
    writer.writerow(fieldnames)
    for key, value in tally2.items():
        writer.writerow([key] + [value]) 

# Get the quantities that these top ingredients usually come in
use_ingredients = tally2.most_common(avg_ingredients_count)
ingredient_list = [''.join(x[0]) for x in use_ingredients]    

# Find all occurrences of these ingredients in our consolidated list
with open('ingredient_measures.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    fieldnames=['Ingredient','Count']
    writer.writerow(fieldnames)
for food_item in ingredient_list:
    indices = [i for i, x in enumerate(consolidated_list) if x == food_item]
    ingredient_context = [mass_text[i] for i in indices]
    with open('ingredient_measures.csv','a') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(0,len(indices)):
            writer.writerow([food_item] + [ingredient_context[i]])
        

## Convert the list into a dataframe- number
#flour_list = []
#butter_list = []
#sugar_list = []
#egg_list = []
#misc = []
#salt_list = []
#vanilla_list = []
#chocolate_chip_list = []
#shortening_list = []
#buttermilk_list = []
#pb_list = []
#bs_list = []
#bp_list = []
#nut_list = []
#milk_list = []
#oat_list = []
#chocolate_list = [] 
#cinna_list = []
#graham_list = []
#water_list = []
#corn_syrup_list = []
#raisin_list = []
#coconut_list = []
#cream_list = []
#apple_list = []
#cocoa_list = []
#veg_oil_list = []
#cc_list = []
#marg_list = []
#sour_cream_list = []
#toffee_list = []
#banana_list = []
#molasses_list = []
#rice_list = []
#extract_list = []
#cherry_list = []
#cranberry_list = []
#coffee_list = []
#mallow_list = []
#honey_list = []
#caramel_list = []
#lemon_list = []
#candy_list = []
#seed_list = []
#cooking_spray_list = []
#baking_mix_list = []
#juice_list = []
#
#
## Get all the occurrences of butter
#for item in mass_text:
#    print(item)
#    item = item.lower()
#    if 'flour' in item:
#        flour_list.append(item)
#    elif 'shortening' in item:
#        shortening_list.append(item)
#    elif 'buttermilk' in item:
#        buttermilk_list.append(item)
#    elif 'peanut butter' in item:
#        pb_list.append(item)
#    elif 'butter' in item:
#        butter_list.append(item)
#    elif'sugar' in item:
#        sugar_list.append(item)
#    elif 'baking soda' in item:
#        bs_list.append(item)
#    elif 'baking powder' in item:
#        bp_list.append(item)
#    elif 'milk' in item:
#        milk_list.append(item)
#    elif 'nuts' in item or 'pecan' in item or 'pistachios' in item or 'almonds' in item or 'walnut' in item:
#        nut_list.append(item)
#    elif 'oat' in item:
#        oat_list.append(item)
#    elif 'egg' in item:
#        egg_list.append(item)
#    elif 'salt' in item:
#        salt_list.append(item)
#    elif 'vanilla' in item:
#        vanilla_list.append(item)
#    elif 'chocolate chip' in item or 'morsels' in item or 'chips' in item:
#        chocolate_chip_list.append(item)
#    elif 'chocolate' in item:
#        chocolate_list.append(item)
#    elif 'cocoa powder' in item:
#        cocoa_list.append(item)
#    elif 'cinnamon' in item:
#        cinna_list.append(item)
#    elif 'graham cracker' in item:
#        graham_list.append(item)
#    elif 'corn syrup' in item:
#        corn_syrup_list.append(item)
#    elif 'water' in item:
#        water_list.append(item)
#    elif 'raisin' in item:
#        raisin_list.append(item)
#    elif 'coconut' in item:
#        coconut_list.append(item)
#    elif 'heavy cream' in item:
#        cream_list.append(item)
#    elif 'applesauce' in item:
#        apple_list.append(item)
#    elif 'vegetable oil' in item or 'canola oil' in item:
#        veg_oil_list.append(item)
#    elif 'cream cheese' in item:
#        cc_list.append(item)
#    elif 'margarine' in item:
#        marg_list.append(item)
#    elif 'sour cream' in item:
#        sour_cream_list.append(item)
#    elif 'toffee' in item:
#        toffee_list.append(item)
#    elif 'banana' in item:
#        banana_list.append(item)
#    elif 'molasses' in item:
#        molasses_list.append(item)
#    elif 'rice' in item:
#        rice_list.append(item)
#    elif 'extract' in item:
#        extract_list.append(item)
#    elif 'cherries' in item:
#        cherry_list.append(item)
#    elif 'cranberr' in item:
#        cranberry_list.append(item)
#    elif 'espresso' in item or 'coffee' in item:
#        coffee_list.append(item)
#    elif 'marshmallow' in item:
#        mallow_list.append(item)
#    elif 'honey' in item:
#        honey_list.append(item)
#    elif 'caramel' in item:
#        caramel_list.append(item)
#    elif 'lemon' in item:
#        lemon_list.append(item)
#    elif 'candy' in item:
#        candy_list.append(item)
#    elif 'seeds' in item:
#        seed_list.append(item)
#    elif 'cooking spray' in item:
#        cooking_spray_list.append(item)
#    elif 'mix' in item:
#        baking_mix_list.append(item)
#    elif 'juice' in item:
#        juice_list.append(item)
#    elif 'cloves' in item:
#        cloves_list.append(item)
#    elif 'nutmeg' in item:
#        nutmeg_list.append(item)
#    elif 'cereal' in item:
#        cereal_list.append(item)
#    elif 'granola' in item:
#        granola_list.append(item)
#                
#    elif item != '':
#        misc.append(item)
#
