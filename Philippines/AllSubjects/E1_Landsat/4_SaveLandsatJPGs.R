library(raster)
library(rgdal)
library(foreach)
library(doParallel)
library(doMC)
registerDoMC(detectCores()-1)

# List the files in the imagery folder
files <- list.files("./Philippines/AllSubjects/E1_Landsat/data/imagery/", full.names = TRUE)
length(files)

# Read in the data frame and split into pass and fail classes
y1314 <- read.csv("./Philippines/AllSubjects/E1_Landsat/data/y1314_AllSubjects.csv")
fail <- y1314[y1314$intervention == 1,]
pass <- y1314[y1314$intervention == 0,]

# For each image, save it as a natural color PNG and sort it into a pass of fail folder
foreach(i = 1:5875) %dopar% {  
	
  id <- base::substr(files[i], 63, 68)
  rast <- raster::brick(files[i])
  school <- y1314[y1314$school_id == id,]
  int <- school$intervention
	
	print(id)

  if (int == 0) {
      file_name <- paste("./Philippines/AllSubjects/E1_Landsat/data/pass/", id, "_", school$intervention, ".jpg", sep = '')
  } else if (int == 1) {
      file_name <- paste("./Philippines/AllSubjects/E1_Landsat/data/fail/", id, "_", school$intervention, ".jpg", sep = '')
  }
  
  
  tryCatch(
    
    {
			
			print(paste("saving file:", file_name))
      
      jpeg(file_name, width = 224, height = 224)
      plotRGB(rast,
           r = 3, g = 2, b = 1,
           stretch = "lin",
           axes = FALSE, frame = FALSE)
      dev.off()
      
    },
    
      error=function(cond) {
        print(paste(file_name, "would not save."))
        
    }
    
  )
  
}


# Check to make sure all iamges saved
fail_files <- list.files("./Philippines/AllSubjects/E1_Landsat/data/fail/", full.names = TRUE)
pass_files <- list.files("./Philippines/AllSubjects/E1_Landsat/data/pass/", full.names = TRUE)

length(fail_files)
length(pass_files)