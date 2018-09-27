### Playing with shapefiles

library(raster)
library(sp)
library(sf)
library(rgdal)

dirpath = '/exports/csce/datastore/geos/users/s1326314/rbg_analysis'
shapefiles = list.files(paste0(dirpath, "/raw_data/site1/raw_shpfiles"),pattern = ".shp",full.names = TRUE)

# Open layer (e.g. raster) with coordiante system you want to convert to
temp = raster('/home/s1326314/rbg_analysis/landsat/LC08_L1TP_182058_20180523_20180605_01_T1.tar/LC08_L1TP_182058_20180523_20180605_01_T1_B10.TIF')
newProj = as.character(crs(temp))

for (i in 1:length(shapefiles) ) {   
  shp = shapefiles[i] # Get shapefile path
  print(shp)
  # sp::spTransform()  #  [package]::[function in said pacakge] - not necessary, but good form and needed if function name is common to multiple packages
  rShp =  shapefile(shp) # First load the shapefile
  
  sf_shp <- st_as_sf(rShp) 
  sf_polygons <- st_polygonize(sf_shp)
  shp_polygons <- as(sf_polygons, "Spatial")
  
  newShp = sp::spTransform(shp_polygons , newProj ) # then project it
  # Export the shapefile to a new folder called "projected" in your shapefile folder
  writeOGR(newShp, paste0( dirname(shp), "/projected/",basename(shp)), layer = basename(shp), driver = "ESRI Shapefile", overwrite_layer = TRUE )
}    

