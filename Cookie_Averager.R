library(ggplot2)
library(dplyr)
library(reshape2)

df <- read.csv("P:\\NLP\\Pudding_Cookie\\ingredient_measures_AllRecipes.csv")
df <- df[!(is.na(df$Ingredient) | df$Ingredient==""), ]

# Get the whole ingredient list
ingred_list <- unique(df$Ingredient)

# For all rows, split the number from the unit
vars <- colsplit(df$Text, " ", c("Quantity","Description"))
df$Quantity <- as.numeric(vars$Quantity)
df$Description <- vars$Description


# Find the unit
df <- mutate(df, Unit = ifelse(grepl("cup",Description),"cup",
                               ifelse(grepl("tablespoon", Description),"tablespoon", 
                                      ifelse(grepl("teaspoon", Description), "teaspoon",
                                             ifelse(grepl("ounce", Description), "ounce",
                                                    ifelse(grepl("pound", Description), "pound",
                                                           ifelse(grepl("egg",Description), "egg", "other")))))))
# Make a table to see the distribution of units and see if anything is uncategorized
table(df$Unit)
df$Quantity


# Which unit is the most popular?
freqfunc <- function(x, n){
  tail(sort(table(unlist(strsplit(as.character(x), ", ")))), n)
}

###### Conversion functions ###########
tbsp2cup <- function(x){
  tbsp_ix <- which(x$Unit == "tablespoon")
  amount <- x[tbsp_ix, 5]
  scaled_amount <- amount*0.0625
  x[tbsp_ix,5] <- scaled_amount
  x[tbsp_ix,7] <- "cup"
  return(x)
}
tsp2cup <- function(x){
  tbsp_ix <- which(x$Unit == "teaspoon")
  amount <- x[tbsp_ix, 5]
  scaled_amount <- amount*0.0208333
  x[tbsp_ix,5] <- scaled_amount
  x[tbsp_ix,7] <- "cup"
  return(x)
}
tsp2tbsp <- function(x){
  tbsp_ix <- which(x$Unit == "teaspoon")
  amount <- x[tbsp_ix, 5]
  scaled_amount <- amount*(1/3)
  x[tbsp_ix,5] <- scaled_amount
  x[tbsp_ix,7] <- "tablespoon"
  return(x)
}
tbsp2tsp <- function(x){
  tbsp_ix <- which(x$Unit == "tablespoon")
  amount <- x[tbsp_ix, 5]
  scaled_amount <- amount*3
  x[tbsp_ix,5] <- scaled_amount
  x[tbsp_ix,7] <- "teaspoon"
  return(x)
}


cup2tbsp <- function(x){
  tbsp_ix <- which(x$Unit == "cup")
  amount <- x[tbsp_ix, 5]
  scaled_amount <- amount/0.0625
  x[tbsp_ix,5] <- scaled_amount
  x[tbsp_ix,7] <- "tablespoon"
  return(x)
}
cup2tsp <- function(x){
  tbsp_ix <- which(x$Unit == "cup")
  amount <- x[tbsp_ix, 5]
  scaled_amount <- amount/0.0208333
  x[tbsp_ix,5] <- scaled_amount
  x[tbsp_ix,7] <- "teaspoon"
  return(x)
}
pkg2oz <- function(x){
  tbsp_ix <- which(x$Unit == "ounce")
  # Is it in ounces already or is it describing a package?
  df_tmp <- subset(x, x$Unit == "ounce")
  y <- which(grepl("[[:digit:]]",df_tmp[,3]))
  amount <- df_tmp[y, 2]
  regexp <- "[[:digit:]]+\\.?[[:digit:]]+"
  scale_factor <- as.numeric(str_extract(df_tmp[y,3],regexp))
  scaled_amount = amount * scale_factor
  df_tmp[y,2] <- scaled_amount
  df_tmp[y,3] <- paste("ounces" , df_tmp[1,1])
  x[tbsp_ix,] <- df_tmp
  return(x)
}

oz2cup <- function(x){
  tbsp_ix <- which(x$Unit == "ounce")
  amount <- x[tbsp_ix, 5]
  scaled_amount <- amount/8
  x[tbsp_ix,5] <- scaled_amount
  x[tbsp_ix,7] <- "cup"
  return(x)
}
pd2oz <- function(x){
  tbsp_ix <- which(x$Unit == "pound")
  amount <- x[tbsp_ix, 5]
  scaled_amount <- amount/16
  x[tbsp_ix,5] <- scaled_amount
  x[tbsp_ix,7] <- "ounce"
  return(x)
}

cup2oz <- function(x){
  tbsp_ix <- which(x$Unit == "cup")
  amount <- x[tbsp_ix, 2]
  scaled_amount <- amount*8
  x[tbsp_ix,2] <- scaled_amount
  x[tbsp_ix,4] <- "ounce"
  return(x)
  
}
# See which unit is most popular for each ingredient
ingred_list <- unique(df$Ingredient)
ingred_list

# For each, convert to a common unit
df_choc <- subset(df, Ingredient == "chocolate chip")
table(df_choc$Unit)
df_choc <- pd2oz(df_choc)
df_choc <- oz2cup(df_choc)
hist(df_choc$Quantity)

df_egg <- subset(df,Ingredient == "egg")

df_bs <- subset(df,Ingredient == "baking soda")
table(df_bs$Unit)
df_bs <- cup2tsp(df_bs)

df_sugar <- subset(df, Ingredient == "sugar")
table(df_sugar$Unit)
df_sugar <- tbsp2cup(df_sugar)

df_ve <- subset(df, Ingredient == "vanilla")
table(df_ve$Unit)
df_ve <- cup2tbsp(df_ve)
df_ve <- tbsp2tsp(df_ve)


df_flour <- subset(df, Ingredient == "all purpose flour") 
table(df_flour$Unit)

df_salt <- subset(df, Ingredient == "salt")
table(df_salt$Unit)
df_salt <- tbsp2tsp(df_salt)

df_brsug <- subset(df, Ingredient == "brown sugar")
table(df_brsug$Unit)
df_brsug <- tbsp2cup(df_brsug)

df_butter <- subset(df, Ingredient == "butter")
table(df_butter$Unit)
df_butter <- tbsp2cup(df_butter)

df_walnuts <- subset(df, Ingredient == "walnut")
table(df_walnuts$Unit)


scaled_df <- rbind(df_walnuts,df_butter,df_brsug, df_salt, df_flour, df_ve, df_egg, df_bs, df_sugar, df_choc)
scaled_df$Quantity <- as.numeric(scaled_df$Quantity)
scaled_df$Rating <- as.numeric(scaled_df$Rating)
scaled_df <- na.omit(scaled_df)
scaled_df <- subset(scaled_df, Quantity <= 25)
scaled_df$weighted <- scaled_df$Quantity * scaled_df$Rating
summary_stat <- scaled_df %>% group_by(Ingredient) %>% summarise(mean = mean(Quantity, na.rm = TRUE),
                                                                 median = median(Quantity, na.rm = TRUE),
                                                                 w_mean2 = weighted.mean(Quantity, Rating),
                                                                 
                                                                 )
summary_stat

hist(scaled_df$Rating)

sub <- subset(scaled_df, Ingredient == "all purpose flour")
weighted.hist(sub$Quantity,sub$Rating)
hist(sub$Quantity)

ggplot(scaled_df, aes(Ingredient, Quantity, colour = Rating)) +
  geom_quasirandom()


# NOT RUN {
## GPA from Siegel 1994
wt <- c(5,  5,  4,  1)/15
x <- c(1,2,3,4)
xm <- weighted.mean(x, wt)
xm
xm <- sum(wt*x)/sum(wt)
xm
# }
