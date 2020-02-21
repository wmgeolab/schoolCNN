library(rgdal)
library(leaflet)
library(raster)
library(rgeos)
library(sp)
library(parallel)
library(snow)



clip_rasters <- function(files_list, shapefile, destination) {
  
  for (folder in files_list) {
    
    lbands <- list.files(folder,
                         pattern = glob2rx("*_B*.TIF$"),
                         full.names = TRUE)
    lbands <- grep("_B[2-4].TIF", lbands, value = TRUE)
    print(lbands)
    
    print("Stacking Rasters")
    landsat_stack_csf <- stack(lbands) # Stack the data
    
    print("Bricking Rasters")
    landsat_csf_br <- brick(landsat_stack_csf) # Turn the raster stack into a brick
    
    #plot(landsat_csf_br)
    landsat_csf_br # View brick attributes
    
    print("Projecting Raster")
    landsat_csf_br <- projectRaster(landsat_csf_br, crs = "+proj=utm +zone=24 +datum=WGS84 +units=m +no_defs +ellps=WGS84 +towgs84=0,0,0")
    
    int <- intersect(shapefile, landsat_csf_br) # Find the schools that overlap with the current raster

    print(int)
    
    a <- 0
		
		if (is.null(int) == FALSE) {
    
			for (school in 1:nrow(int)) {

				selected <- int[school,]

				extract <- raster::crop(landsat_csf_br, selected)

				file_name <- paste(destination, selected$schol_d, '.tif', sep = '')

				print(paste("FILE #", a, " out of ", dim(int)[1], ": ", file_name, sep = ''))

				if (!file.exists(file_name)) {
					writeRaster(extract, filename = file_name)
				} else {
					if (object.size(file_name) < (object.size(extract))) {
						writeRaster(extract, filename = file_name, overwrite = TRUE)
					}
				}

				a = a + 1

			}
			
		}
        
  } 
  
}




# Read in the school squares shapefile
sb <- readOGR("./Brazil/E1_Landsat/data/sb/y15_Brazil_sb.shp")
sb <- sp::spTransform(sb, "+proj=utm +zone=24 +datum=WGS84 +units=m +no_defs +ellps=WGS84 +towgs84=0,0,0")
class(sb)


y12_13_folders <- list.files("./Brazil/E1_Landsat/data/Landsat/", full.name = TRUE)

ncores <- detectCores() - 1
beginCluster(ncores)

clusterR(clip_rasters(y12_13_folders, sb, "./Brazil/E1_Landsat/data/imagery/"))

endCluster()
