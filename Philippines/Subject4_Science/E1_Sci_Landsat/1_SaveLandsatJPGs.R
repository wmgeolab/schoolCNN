library(raster)
library(rgdal)
library(foreach)
library(doParallel)
library(doMC)
registerDoMC(detectCores()-1)


files <- list.files("./Philippines/AllSubjects/E1_Sci_Landsat/data/imagery/", full.names = TRUE)
length(files)

y1314 <- read.csv("./Philippines/Subject4_Science/E1_Sci_Landsat/data/y1314_Science.csv")
fail <- y1314[y1314$intervention == 1,]
pass <- y1314[y1314$intervention == 0,]


foreach(i = 1:5875) %dopar% {  
	
  id <- base::substr(files[i], 63, 68)
  rast <- raster::brick(files[i])
  school <- y1314[y1314$school_id == id,]
  int <- school$intervention

  if (int == 0) {
      file_name <- paste("./Philippines/Subject4_Science/E1_Sci_Landsat/data/pass/", id, "_", school$intervention, ".jpg", sep = '')
  } else if (int == 1) {
      file_name <- paste("./Philippines/Subject4_Science/E1_Sci_Landsat/data/fail/", id, "_", school$intervention, ".jpg", sep = '')
  }
  
  tryCatch(
    
    {
			
#			print(paste("saving file:", file_name))
      
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


fail_files <- list.files("./Philippines/Subject4_Science/E1_Sci_Landsat/data/fail/", full.names = TRUE)
pass_files <- list.files("./Philippines/Subject4_Science/E1_Sci_Landsat/data/pass/", full.names = TRUE)

length(fail_files)
length(pass_files)