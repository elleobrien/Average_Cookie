# Average_Cookie

This repository contains data and analyses behind the story, "Baking the Most Average Chocolate Chip Cookie", featured in The Pudding. The directory structure is as follows:

**Scraped_Recipes** contains every scraped chocolate chip cookie recipe, sorted by source (allrecipes.com, epicurious.com, or other) in an individual .txt file. 

The scripts in the home directory indexed 0a-0c_Incredient_Analysis_*.py are used to process text data from the scraped recipes into analyzable form. The outputs of these scripts is written to the **Aggregated_Data** directory. 

**Aggregated_Data** contains .csv and .txt files of the recipe dataset at various stages of processing:
+ 0_ingredient_measures* is the compiled list of ingredients in raw form from each source
+ 1_Ingredient_measures_all aggregates the lists of ingredients from each source into one document
+ 2_Scaled_Units* is made by scaling all the ingredient counts to yield the same number of cookies per recipe
+ 3_All_ingredient_Average is the average count of each ingredient in the dataset, after averaging the values in 2_Scaled_Units_Cleaned.csv
+ 4_All_Directions.txt gives every set of recipe instructions in the dataset in one newline-delimited file.
Note that the suffix "_Cleaned" indicates that the file was manually inspected and edited for irregularities.

**Average** Files indexed 1-6 give the entire pipeline for estimating the average count of each ingredient, clustering sentences in recipe instructions by word embeddings, and making preliminary visualizations with the ggplot2 library for R. 

**Markov** The file Ngram_Markov_Model.py contains the complete code to generate recipes using a Markov language model with several different parameterizations. 

**RNN** This folder contains the output of an RNN model. The RNN model (not provided in this repo) is a clone of jcjohnson's torch-rnn repo https://github.com/jcjohnson/torch-rnn



