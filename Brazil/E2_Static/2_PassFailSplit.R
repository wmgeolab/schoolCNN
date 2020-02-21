library(raster)
library(rgdal)
library(foreach)
library(doParallel)
library(doMC)
registerDoMC(detectCores()-1)


files <- list.files("./Brazil/E2_Static/data/imagery/", full.names = TRUE)	
length(files)

y1314 <- read.csv("./Brazil/E2_Static/data/y15_Brazil.csv")

table(y1314$intervention)


for (i in 1:5464) {
  
  id <- base::substr(files[i], 34, 41)
  school <- subset(y1314, school_id == as.numeric(id))
  int <- school$intervention
	
	print(int)
  
  if (int == 0) {
      file.copy(files[i], "./Brazil/E2_Static/data/pass/")
  } else if (int == 1) {
      file.copy(files[i], "./Brazil/E2_Static/data/fail/")
  }
  
}


pass_files <- list.files("./Brazil/E2_Static/data/pass/", full.names = TRUE)
fail_files <- list.files("./Brazil/E2_Static/data/fail/", full.names = TRUE)

length(pass_files)
length(fail_files)
