library(rgdal)
library(raster)
library(rgeos)
library(sp)
library(foreach)
library(doParallel)
library(doMC)
registerDoMC(detectCores()-1)


# Function to clip each boxe in the school boxes shapefile from the mosaiced raster
clip_rasters <- function(rast, shapefile, destination) {

      a <- 0
      
      foreach(school = 1:nrow(shapefile)) %dopar% {
				      
            selected <- shapefile[school,]
            extract <- raster::crop(rast, selected)
            file_name <- paste(destination, selected$school_id, '.tif', sep = '')
					
            raster::writeRaster(extract, filename = file_name)

            a <- a + 1
				
					print(a)

      }

}
  

# Read in the school squares shapefile
sb <- readOGR('./Philippines/AllSubjects/E1_Landsat/data/shp/y1314_AllSubjects_sb.shp')
sb <- sp::spTransform(sb, "+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0")
class(sb)

r <- raster::brick("./Philippines/AllSubjects/E1_Landsat/data/mosaic_proj.tif")

# Rename the shapefile columns
colnames(sb@data) <- c("school_id", "overall_mean", "intervention", "latitude", "longitude")

clip_rasters(r, sb, './Philippines/AllSubjects/E1_Landsat/data/imagery/')
