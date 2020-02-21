library(rgdal)


create_boxes <- function(shp) {

  colnames(shp@data) <- c("school_id", "overall_mean", "intervention", "latitude", "longitude")
  
  # Read in Shapefile
  shp <- shp[!duplicated(shp$school_id), ]
  
  # Check projection
  print(crs(shp))
  
  # Define new projection
  utm_proj <- "+proj=utm +zone=51 +datum=WGS84 +units=m +no_defs +ellps=WGS84 +towgs84=0,0,0"

  # Project Data
  shp_utm <- spTransform(shp, utm_proj)

  
  print("made it to here")
  # Create data frame and remove duplicates
  df <- as.data.frame(shp_utm)
  df <- df[!duplicated(df$school_id), ]

  # Fix column names
  colnames(df) <- c("school_id", "overall_mean", "intervention", 
                    "latitude", "longitude",
                    "utm_latitude", "utm_longitude")

  # Convert columns to numeric
  df$utm_latitude <- as.numeric(df$utm_latitude)
  df$utm_longitude <- as.numeric(df$utm_longitude)

  print(df)

  # Calculate square bounding box around school
  df$bbox_ur_lat <- df$utm_latitude + 3360
  df$bbox_ur_long <- df$utm_longitude + 3360

  df$bbox_lr_lat <- df$utm_latitude + 3360
  df$bbox_lr_long <- df$utm_longitude - 3360

  df$bbox_ll_lat <- df$utm_latitude - 3360
  df$bbox_ll_long <- df$utm_longitude - 3360

  df$bbox_ul_lat <- df$utm_latitude - 3360
  df$bbox_ul_long <- df$utm_longitude + 3360

  # Convert dataframe to SpatialPolygons
  polys <- list()

  for(i in 1:nrow(df)) {

    row <- df[i,]

    m1 <- row$bbox_ur_lat
    m2 <- row$bbox_ur_long
    m3 <- row$bbox_lr_lat
    m4 <- row$bbox_lr_long
    m5 <- row$bbox_ll_lat
    m6 <- row$bbox_ll_long
    m7 <- row$bbox_ul_lat
    m8 <- row$bbox_ul_long

    coords <- matrix(c(m1, m2,
                       m3, m4,
                       m5, m6,
                       m7, m8),
                     ncol = 2, byrow = TRUE)

    polys <- rlist::list.append(polys, coords)

  }

  ids <- as.character(df$school_id)

  # Crete Polgyosn and SpatialPolygonsDataFrame
  p <- lapply(polys, Polygon)
  ps <- lapply(seq_along(p), function(i) Polygons(list(p[[i]]), ID = ids[i]))
  sps <- SpatialPolygons(ps)
  sps_df <- SpatialPolygonsDataFrame(sps, data.frame(x = rep(NA, length(p)), row.names = ids))

  plot(sps_df, col=rainbow(50, alpha=0.5))
  plot(shp_utm, add = TRUE)

  # Assign a projection to the SPDF and then reproject it
  crs(sps_df) <- "+proj=utm +zone=51 +datum=WGS84 +units=m +no_defs +ellps=WGS84 +towgs84=0,0,0"
  sps_df_deg <- spTransform(sps_df, "+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0")

  sps_df_deg@data <- shp@data

  return(sps_df_deg)

}
							 

# Read in school points shapefile							 
sp <- readOGR("./Philippines/AllSubjects/E1_Landsat/data/shp/y1314_AllSubjects_sp.shp")

# Create 224x224px boxes around each school
sb <- create_boxes(sp)
							 
# Save school boxes shapefile
writeOGR(sb, dsn = "./Philippines/AllSubjects/E1_Landsat/data/shp/y1314_AllSubjects_sb.shp", layer = "y1314_AllSubjects_sb", driver = "ESRI Shapefile", overwrite_layer = TRUE)


							 