library(classInt)
library(leaflet)
library(rgdal)
library(sp)

# Read in Grade 6 and 10 data
df6 <- read.csv("./Brazil/data/BrazilCleaned.py")

dim(df6)

kmeans_overall <- classIntervals(df6$passing, 2, style = "kmeans")

hist(df6$passing)

range(df6$mean)

# Subset columns
final_df <- df6[c("school_id", "passing", 'latitude', 'longitude')]


# Assign interventon booleans based on above kmeans break 
final_df$intervention <- NA
final_df$intervention[final_df$passing < mean(final_df$passing)] <- 1
final_df$intervention[final_df$passing >= mean(final_df$passing)] <- 0

table(final_df$intervention)


head(final_df)

# Write final CSV
write.csv(final_df, "./Brazil/E1_Landsat/data/y15_Brazil.csv", row.names=FALSE)
write.csv(final_df, "./Brazil/E2_Static/data/y15_Brazil.csv", row.names=FALSE)
write.csv(final_df, "./Brazil/E3_StreetView/data/y15_Brazil.csv", row.names=FALSE)

# Create shapefile
coords <- cbind(final_df$longitude, final_df$latitude)
sp <- SpatialPoints(coords)
spdf <- SpatialPointsDataFrame(coords, final_df, proj4string = CRS("+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0"))

# Write shapefile
writeOGR(spdf, dsn = "./Brazil/E1_Landsat/data/sp/y15_Brazil.shp", layer = "y15_Brazil", driver = "ESRI Shapefile", overwrite_layer = TRUE)
