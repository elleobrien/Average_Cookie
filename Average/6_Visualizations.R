library(ggplot2)

rm(list = ls())

# Read in the scaled ingredients
df <- read.csv("../Aggregated_Data/2_Scaled_Units_Cleaned.csv", row.names = NULL)
df$Quantity <- as.numeric(as.character(df$Quantity))

# How many ingredients are on average in a recipe?
num_ingred <- df %>% group_by(Recipe_Index) %>% summarise(num = n())
mean(num_ingred$num) # About 10

# Get the tenmost frequent ingredients
ingred_freq <- df %>% group_by(Ingredient) %>% summarise(count = n())
# Get top ingredients
top_ten <- head(ingred_freq[order(ingred_freq$count, decreasing= T),], n = 10)
# Get the average quantities of each of these
ingred_list <- top_ten$Ingredient

# Make faceted histograms of each ingredient count
ggplot(subset(df, Ingredient %in% ingred_list), aes(Quantity)) + geom_histogram(aes(fill=Ingredient)) +
  facet_wrap(~Ingredient,scales = "free_x")+
  theme(legend.position="none")

##### Now, let's look at the relative frequency of various ingredients
freq_df_head <- head(ingred_freq[order(ingred_freq$count, decreasing= T),], n = 15)
ggplot(freq_df_head, aes(x = reorder(Ingredient, count),y = count)) + geom_bar(stat="identity")+
  coord_flip()+
  ylab("Frequency in Recipes")+
  xlab("Ingredient")

# What kinds of chocolate are people using?
df_choc <- subset(df, Ingredient == "chocolate chip")
# Find the unit
chip_df <- mutate(df_choc, kind = ifelse(grepl("milk",Text),"milk",
                                         ifelse(grepl("dark", Text),"dark", 
                                                ifelse(grepl("bittersweet", Text), "bittersweet",
                                                       ifelse(grepl("white", Text), "white", "semisweet")))))


chip_df2 <- chip_df %>%
  group_by(kind) %>%
  summarise(count = n())

#chip_df2 <- chip_df %>% droplevels() %>% dplyr::filter(count > 1)
#levels(chip_df$kind)
chip_df2$kind <- factor(chip_df2$kind, 
                        levels = c("white","milk","semisweet","bittersweet","dark"))
levels(chip_df2$kind)
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


############################################################################
#### Visualize the recipe instruction space #######
df_recipe <- read.csv("Sentence_PCA.csv")
setnames(df_recipe, old=c("Coord1","Coord2"), new=c("PC1", "PC2"))

ggplot(df_recipe, aes(PC1,PC2)) + geom_point(aes(colour = as.factor(Cluster)))

#gg<- data.frame(cluster =factor(df_recipe$Cluster), x= df_recipe$PC1, y = df_recipe$PC2)
centroids <- aggregate(cbind(PC1,PC2) ~ Cluster, data = df_recipe, mean)
df_recipe <- merge(df_recipe, centroids, by = "Cluster", suffixes = c("",".centroid"))



### Plot all the points bursting from their centroid
ggplot(df_recipe, aes(PC1,PC2, color=as.factor(Cluster)))+
  geom_point(size=3) +
  geom_point(data=centroids, size=4) +
  geom_segment(aes(x=PC1.centroid, y=PC2.centroid, xend=PC1, yend=PC2))


