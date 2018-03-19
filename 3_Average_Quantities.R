rm(list = ls())

# Read in the data frame
df <- read.csv("Scaled_Units.csv", row.names = NULL)
df$Quantity <- as.numeric(as.character(df$Quantity))

# How many recipes are there in the databse?
n_recipes = length(unique(df$Recipe_Index))

# How many ingredients are in a recipe on average?
num_ingred <- df %>% group_by(Recipe_Index) %>% summarise(num = n())
mean(num_ingred$num)

# List of ingredients
ingred_list <- unique(df$Ingredient)


padded_avg <- function(x){ 
  quant <- as.vector(x)
  # Pad with zeros
  recipes_using = length(quant)
  recipes_not = n_recipes - recipes_using
  
  if (recipes_not > 0){  pad <- rep(0, length.out = recipes_not) 
  tmp_pad <- append(quant, pad)
  padded_avg <- mean(tmp_pad)}
  else{
    padded_avg <- mean(quant)
  }

  return(padded_avg)
  }

# Get the padded average for all ingredients
df_sum <- df %>% group_by(Ingredient, Unit) %>% summarise(mean = padded_avg(Quantity))
  
# Print it out! 
write.csv(df_sum, "All_Ingredient_Average.csv")

# Now, what if we just used the top 10 most common ingredients?
ingred_freq <- df %>% group_by(Ingredient) %>% summarise(count = n())
# Get top ingredients
head(ingred_freq[order(ingred_freq$count, decreasing= T),], n = 10)


