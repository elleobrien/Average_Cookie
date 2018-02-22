library(ggplot2)
library(dplyr)
library(reshape2)

df <- read.csv("P:\\NLP\\Pudding_Cookie\\ingredient_measures.csv")
df <- df[!(is.na(df$Ingredient) | df$Ingredient==""), ]


# Get the whole ingredient list
ingred_list <- unique(df$Ingredient)

# For all rows, split the number from the unit
vars <- colsplit(df$Count, " ", c("Quantity","Description"))
df$Quantity <- vars$Quantity
df$Description <- vars$Description
df$Count <- NULL

# Find the unit
df <- mutate(df, Unit = ifelse(grepl("cup",Description),"cup",
                                    ifelse(grepl("tablespoon", Description),"tablespoon", 
                                      ifelse(grepl("teaspoon", Description), "teaspoon",
                                             ifelse(grepl("ounce", Description), "ounce",
                                                ifelse(grepl("pound", Description), "pound",
                                                  ifelse(grepl("egg",Description), "egg", "other")))))))
# Make a table to see the distribution of units and see if anything is uncategorized
table(df$Unit)


# Which unit is the most popular?
freqfunc <- function(x, n){
  tail(sort(table(unlist(strsplit(as.character(x), ", ")))), n)
}

###### Conversion functions ###########
tbsp2cup <- function(x){
  tbsp_ix <- which(x$Unit == "tablespoon")
  amount <- x[tbsp_ix, 2]
  scaled_amount <- amount*0.0625
  x[tbsp_ix,2] <- scaled_amount
  x[tbsp_ix,4] <- "cup"
  return(x)
}
tsp2cup <- function(x){
  tbsp_ix <- which(x$Unit == "teaspoon")
  amount <- x[tbsp_ix, 2]
  scaled_amount <- amount*0.0208333
  x[tbsp_ix,2] <- scaled_amount
  x[tbsp_ix,4] <- "cup"
  return(x)
}
tsp2tbsp <- function(x){
  tbsp_ix <- which(x$Unit == "teaspoon")
  amount <- x[tbsp_ix, 2]
  scaled_amount <- amount*(1/3)
  x[tbsp_ix,2] <- scaled_amount
  x[tbsp_ix,4] <- "tablespoon"
  return(x)
}
tbsp2tsp <- function(x){
  tbsp_ix <- which(x$Unit == "tablespoon")
  amount <- x[tbsp_ix, 2]
  scaled_amount <- amount*3
  x[tbsp_ix,2] <- scaled_amount
  x[tbsp_ix,4] <- "teaspoon"
  return(x)
}


cup2tbsp <- function(x){
  tbsp_ix <- which(x$Unit == "cup")
  amount <- x[tbsp_ix, 2]
  scaled_amount <- amount/0.0625
  x[tbsp_ix,2] <- scaled_amount
  x[tbsp_ix,4] <- "tablespoon"
  return(x)
}
cup2tsp <- function(x){
  tbsp_ix <- which(x$Unit == "cup")
  amount <- x[tbsp_ix, 2]
  scaled_amount <- amount/0.0208333
  x[tbsp_ix,2] <- scaled_amount
  x[tbsp_ix,4] <- "teaspoon"
  return(x)
}
pkg2oz <- function(x){
  tbsp_ix <- which(x$Unit == "ounce")
  # Is it in ounces already or is it describing a package?
  df_tmp <- x[tbsp_ix,]
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
  amount <- x[tbsp_ix, 2]
  scaled_amount <- amount/8
  x[tbsp_ix,2] <- scaled_amount
  x[tbsp_ix,4] <- "cup"
  return(x)
}
pd2oz <- function(x){
  tbsp_ix <- which(x$Unit == "pound")
  amount <- x[tbsp_ix, 2]
  scaled_amount <- amount/16
  x[tbsp_ix,2] <- scaled_amount
  x[tbsp_ix,4] <- "ounce"
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
df_choc <- subset(df, Ingredient == "chocolate chips")
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

df_ve <- subset(df, Ingredient == "vanilla extract")
table(df_ve$Unit)
df_ve <- cup2tbsp(df_ve)
df_ve <- tbsp2tsp(df_ve)


df_flour <- subset(df, Ingredient == "all-purpose flour") 
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

df_walnuts <- subset(df, Ingredient == "walnuts")
table(df_walnuts$Unit)

scaled_df <- rbind(df_walnuts,df_butter,df_brsug, df_salt, df_flour, df_ve, df_egg, df_bs, df_sugar, df_choc)



mode <- function(x) {
  ux <- unique(x)
  ux[which.max(tabulate(match(x, ux)))]
}


library(modeest)
mlv(y, method = "mfv")
# Get the means of each ingredient
library(bbmle)
m <- mle2(y~dnorm(mean=mu,sd=sd),start=list(mu=1,sd=0.1),data = data.frame(y))
# Hmmmmmm. Maximum likelihood is just too similar to the actual means. Not very interesting. 


summary_stat <- scaled_df %>% group_by(Ingredient) %>% summarise(mean = mean(Quantity),
                                                                 median = median(Quantity),
                                                                 mode = mode(Quantity))

# Make faceted histograms of each ingredient count
ggplot(scaled_df, aes(Quantity)) + geom_histogram(aes(fill=Ingredient)) +
  facet_wrap(~Ingredient,scales = "free_x")+
  theme(legend.position="none")

##### Now, let's look at the relative frequency of various ingredients
freq_df <-read.csv("P:\\NLP\\Pudding_Cookie\\ingredient_tally.csv")
freq_df <- freq_df[order(freq_df$count, decreasing=TRUE),]
freq_df_head <- freq_df[1:20,]

ggplot(freq_df_head, aes(x = reorder(ingredient, count),y = count)) + geom_bar(stat="identity")+
  coord_flip()+
  ylab("Frequency in Recipes")+
  xlab("Ingredient")

# What kinds of chocolate are people using?
#choc_df <- freq_df[grep("chocolate chip", freq_df$ingredient), ]
#mutate(choc_df, type = ifelse("semisweet" %in% ingredient | "semi-sweet" %in% ingredient), "semisweet",
 #      "milk")
# Find the unit
chip_df <- mutate(df_choc, kind = ifelse(grepl("milk",Description),"milk",
                               ifelse(grepl("dark", Description),"dark", 
                                      ifelse(grepl("bittersweet", Description), "bittersweet",
                                             ifelse(grepl("white", Description), "white", "semisweet")))))
                                                           

chip_df2 <- chip_df %>%
  group_by(kind) %>%
  summarise(count = n())

#chip_df2 <- chip_df %>% droplevels() %>% dplyr::filter(count > 1)
#levels(chip_df$kind)
chip_df2$kind <- factor(chip_df2$kind, 
                             levels = c("white","milk","semisweet","bittersweet","dark"))
levels(chip_df2$ingredient)
chip_df2 <- chip_df2 %>% droplevels()
chip_df2 <- na.omit(chip_df2)

# make browns color palette
browns <- c("white", colorRampPalette(c("#8e6f45","#5b3a0f"))(3), "#3d2404")
# display.brewer.pal(5, "BrBG")
# RColorBrewer::brewer.pal(5, "BrBG")

pie <- ggplot(chip_df2)+
  aes(x="",y=count,fill=kind) + 
  geom_bar(stat="identity") + 
  # scale_fill_brewer(palette = "BrBG")+
  scale_fill_manual(values = browns)+
  coord_cartesian(expand = FALSE)+
  coord_polar("y", start=0, theta = )+
  guides(fill = guide_legend(reverse = TRUE))+
  theme_void()
pie

df_egg <- df %>% dplyr::filter(Ingredient == "egg")
  
df_egg$Quantity_rnd <- as.integer(df_egg$Quantity)

ggplot(df_egg)+
  aes(x = Quantity_rnd)+
  geom_dotplot(shape = "0", color = "black", fill = "white", size = 4)

############################################################################
#### Visualize the recipe instruction space #######
df_recipe <- read.csv("P:\\botnik\\Tabloid_Scrapers\\All_Recipes\\PCA_sentences.csv")
#df_recipe[, 1:3] <- sapply(df_recipe[, 1:3], as.factor)
#df_recipe

ggplot(df_recipe, aes(PC1,PC2)) + geom_point(aes(colour = as.factor(Cluster)))

#gg<- data.frame(cluster =factor(df_recipe$Cluster), x= df_recipe$PC1, y = df_recipe$PC2)
centroids <- aggregate(cbind(PC1,PC2) ~ Cluster, data = df_recipe, mean)
df_recipe <- merge(df_recipe, centroids, by = "Cluster", suffixes = c("",".centroid"))
library(ellipse)

gg <- df_recipe
conf.rgn  <- do.call(rbind,lapply(0:6,function(i)
  cbind(cluster=i,ellipse(cov(gg[gg$Cluster==i,2:3]),centre=as.matrix(centroids[i+1,2:3])))))
conf.rgn  <- data.frame(conf.rgn)
conf.rgn$Cluster <- factor(conf.rgn$cluster)


### Plot all the points bursting from their centroid
ggplot(gg, aes(PC1,PC2, color=as.factor(Cluster)))+
  geom_point(size=3) +
  geom_point(data=centroids, size=4) +
  geom_segment(aes(x=PC1.centroid, y=PC2.centroid, xend=PC1, yend=PC2))

#ggplot(data = conf.rgn, aes(PC1,PC2, group = Cluster)) + geom_path()


