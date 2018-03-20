library(ggplot2)
library(dplyr)
library(reshape2)

setwd('../Aggregated_Data')
df1 <- read.csv("ingredient_measures_AllRecipes.csv")
df1$Recipe_Index <- paste0("AR_", df1$Recipe_Index)
df2 <- read.csv("ingredient_measures_Epicurious.csv")
df2$Recipe_Index <- paste0("E_", df2$Recipe_Index)
df3 <- read.csv("ingredient_measures_Misc.csv")
df3$Recipe_Index <- paste0("Misc_", df3$Recipe_Index)

# Bind the dataframes together
big_df <- rbind(df1,df2,df3)

# Remove any rows that have no ingredient description
big_df <- big_df[!(is.na(big_df$Text) | big_df$Text==""), ]

# Remove any rows that have no recipe index
big_df <- big_df[!(is.na(big_df$Recipe_Index) | big_df$Recipe_Index==""), ]

# Remove incomplete rows
#big_df <- na.omit(big_df)

# Remove any commas from the text 
big_df$Text <- gsub(",","",big_df$Text)


#Save as a big data frame for manual editing
write.table(big_df, file = "1_ingredient_measures_All.csv", quote = FALSE, row.names = FALSE, dec = '.', sep = ',') 


