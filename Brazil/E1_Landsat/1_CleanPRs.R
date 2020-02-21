library(rgdal)

# We ran the intersectin of the Landsat Path/Row shapefile with the Brazil schools 
# in QGIS and read in the interescting Path/Row shapefile here to rename the columns
shp <- readOGR("./Brazil/E1_Landsat/data/PathRows/prs.shp")
df <- data.frame(shp@data)
df <- df[c("PATH", "ROW")]
head(df)

write.csv(df, "./Brazil/E1_Landsat/data/PRs.csv")
