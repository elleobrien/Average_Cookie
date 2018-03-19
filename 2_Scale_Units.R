rm(list = ls())

setwd('./Aggregated_Data')
# Read in the data frame
df <- read.csv("ingredient_measures_All_Cleaned.csv", row.names = NULL)
df <- read.csv("ingredient_measures_Misc_Addend.csv", row.names = NULL)

# Remove ingredients from cancelled recipes
# Aren't really plain chocolate chip cookies
excl <- c( "E_95", "E_145", "E_282", "E_294", "E_360","AR_44","AR_81","AR_38")


# E_197 is gluten free. want to get rid of?

df <- subset(df, ! (Recipe_Index %in% excl))

# Get the whole ingredient list
ingred_list <- unique(df$Ingredient)

# Get a count of each type of ingredient
with(droplevels(df), table(Ingredient))

# How many ingredients are included in a recipe on average?
num_ingred <- df %>% group_by(Recipe_Index) %>% summarise(num = n())
mean(num_ingred$num)

# How many recipes are there?
num_recipe <- length(unique(df$Recipe_Index))
num_recipe

# For all rows, split the number from the unit
vars <- colsplit(df$Text, " ", c("Quantity","Description"))
df$Quantity <- as.numeric(vars$Quantity)


# Remove any ingredient that didn't have a quantity attached to it
df <- subset(df, Quantity != "NA")


# Find the unit
df <- mutate(df, Unit = ifelse(grepl("cup",Text),"cup",
                               ifelse(grepl("tablespoon|tbsp", Text),"tablespoon", 
                                      ifelse(grepl("teaspoon|tsp", Text), "teaspoon",
                                             ifelse(grepl("ounce", Text), "ounce",
                                                    ifelse(grepl("pound", Text), "pound",
                                                           ifelse(grepl("egg",Text), "egg", "other")))))))
# Make a table to see the distribution of units and see if anything is uncategorized
table(df$Unit)
df <- subset(df, Unit != "other") # Remove things in unusual units




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
  x[tbsp_ix,6] <- "cup"
  return(x)
}
tsp2cup <- function(x){
  tbsp_ix <- which(x$Unit == "teaspoon")
  amount <- x[tbsp_ix, 5]
  scaled_amount <- amount*0.0208333
  x[tbsp_ix,5] <- scaled_amount
  x[tbsp_ix,6] <- "cup"
  return(x)
}
tsp2tbsp <- function(x){
  tbsp_ix <- which(x$Unit == "teaspoon")
  amount <- x[tbsp_ix, 5]
  scaled_amount <- amount*(1/3)
  x[tbsp_ix,5] <- scaled_amount
  x[tbsp_ix,6] <- "tablespoon"
  return(x)
}
tbsp2tsp <- function(x){
  tbsp_ix <- which(x$Unit == "tablespoon")
  amount <- x[tbsp_ix, 5]
  scaled_amount <- amount*3
  x[tbsp_ix,5] <- scaled_amount
  x[tbsp_ix,6] <- "teaspoon"
  return(x)
}


cup2tbsp <- function(x){
  tbsp_ix <- which(x$Unit == "cup")
  amount <- x[tbsp_ix, 5]
  scaled_amount <- amount/0.0625
  x[tbsp_ix,5] <- scaled_amount
  x[tbsp_ix,6] <- "tablespoon"
  return(x)
}
cup2tsp <- function(x){
  tbsp_ix <- which(x$Unit == "cup")
  amount <- x[tbsp_ix, 5]
  scaled_amount <- amount/0.0208333
  x[tbsp_ix,5] <- scaled_amount
  x[tbsp_ix,6] <- "teaspoon"
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
  x[tbsp_ix,6] <- "cup"
  return(x)
}
pd2oz <- function(x){
  tbsp_ix <- which(x$Unit == "pound")
  amount <- x[tbsp_ix, 5]
  scaled_amount <- amount/16
  x[tbsp_ix,5] <- scaled_amount
  x[tbsp_ix,6] <- "ounce"
  return(x)
}

cup2oz <- function(x){
  tbsp_ix <- which(x$Unit == "cup")
  amount <- x$Quantity
  scaled_amount <- amount*8
  x[tbsp_ix,2] <- scaled_amount
  x[tbsp_ix,4] <- "ounce"
  return(x)
  
}



# For each, convert to a common unit
df_choc <- subset(df, Ingredient == "chocolate chip")
table(df_choc$Unit)
df_choc <- pd2oz(df_choc)
df_choc <- oz2cup(df_choc)
df_choc <- tbsp2cup(df_choc)
hist(df_choc$Quantity)

df_egg <- subset(df,Ingredient == "egg")
hist(df_egg$Quantity)


df_bs <- subset(df,Ingredient == "baking soda")
table(df_bs$Unit)
df_bs <- cup2tsp(df_bs)

df_sugar <- subset(df, Ingredient == "sugar")
table(df_sugar$Unit)
df_sugar <- tbsp2cup(df_sugar)
df_sugar <- tsp2cup(df_sugar)
df_sugar <- oz2cup(df_sugar)

df_ve <- subset(df, Ingredient == "vanilla")
table(df_ve$Unit)
df_ve <- oz2cup(df_ve)
df_ve <- cup2tbsp(df_ve)
df_ve <- tbsp2tsp(df_ve)
hist(df_ve$Quantity)


df_flour <- subset(df, Ingredient == "all purpose flour") 
table(df_flour$Unit)
df_flour <- tbsp2cup(df_flour)
df_flour <- oz2cup(df_flour)


df_salt <- subset(df, Ingredient == "salt")
table(df_salt$Unit)
df_salt <- tbsp2tsp(df_salt)
# Cup is wrong- that is attached to salted nuts
#df_salt <- subset(df_salt, Unit != "cup")

df_brsug <- subset(df, Ingredient == "brown sugar")
table(df_brsug$Unit)
df_brsug <- tbsp2cup(df_brsug)
df_brsug <- oz2cup(df_brsug)

df_butter <- subset(df, Ingredient == "butter")
table(df_butter$Unit)

df_butter <- tbsp2cup(df_butter)
df_butter <- pd2oz(df_butter)
df_butter <- oz2cup(df_butter)


df_walnuts <- subset(df, Ingredient == "walnut")
table(df_walnuts$Unit)

df_milk <- subset(df, Ingredient == "milk")
table(df_milk$Unit)
df_milk <- cup2tbsp(df_milk)


scaled_df <- rbind(df_walnuts,df_milk,df_butter,df_brsug, df_salt, df_flour, df_ve, df_egg, df_bs, df_sugar, df_choc)
scaled_df$Quantity <- as.numeric(scaled_df$Quantity)
scaled_df$Rating <- as.numeric(scaled_df$Rating)


### Add back all the other columns
df_comp <- subset(df, !(Ingredient %in% c("walnut","butter","all purpose flour","baking soda",
                                          "brown sugar", "salt", "vanilla", "egg", "sugar",
                                          "chocolate chip","milk")))

master_df <- rbind(scaled_df, df_comp)
write.csv(master_df, file = "Scaled_Units_add.csv")



# Detect and remove outliers
scaled_df <- within(scaled_df, stan <- ave(Quantity, Ingredient, FUN = stdz)) %>%
  subset(abs(stan) <= 3) # Because anything more than 3 std. deviations out of the mean is likely to be a scaling error, remove these

summary_stat <- scaled_df %>% group_by(Ingredient) %>% summarise(mean = mean(Quantity, na.rm = TRUE),
                                                                 median = median(Quantity, na.rm = TRUE))

summary_stat

