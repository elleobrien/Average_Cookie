# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 18:50:09 2018

@author: andro
"""
import os.path

# This is a script for manual entry of new recipes.

# Ask for the link
link = input("What is the link?\n")

# Ask for the serving size
serves = input("What is the serving size?\n")

# Ask for a rating?
rating = input("Is there a rating? Write NA if not.\n")


# Ask for the ingred list
ingredients = input("What is the ingredient list?\n")

# Ask for the recipe instructions
recipe = input("What are the instructions?\n")


# Write them all to file in the MISC folder
index = 1
fid = 'source_' + str(index) + '.txt'
file_path = "P://NLP//Pudding_Cookie//Misc//" + fid

while os.path.exists(file_path):
    index = index + 1
    fid = 'source_' + str(index) + '.txt.'
    file_path = "P://NLP//Pudding_Cookie//Misc//" + fid


os.chdir("P://NLP//Pudding_Cookie//Misc//")

# Print the source
link_file = fid
with open(link_file, 'w') as f:
    f.write(link)
f.close()

# Print the serving size
serving_file = "servings_" + str(index) + ".txt."
with open(serving_file, 'w') as f:
    f.write(serves)
f.close()

# Print the ingredients
ingred_file = "ingredients_" + str(index) + ".txt."
with open(ingred_file, 'w', encoding = 'utf-8') as f:
    f.write(ingredients)
f.close()

# Print the recipe
recipe_file = "recipe_" + str(index) + ".txt."
with open(recipe_file, 'w', encoding = 'utf-8') as f:
    f.write(recipe)
f.close()

# Print the rating
rating_file = "rating_" + str(index) + ".txt."
with open(rating_file, 'w') as f:
    f.write(rating)
f.close()
    