setwd("D:/Dropbox/Compactness Shared/Data/State Leg Shapefiles")
library(spatial)
library(rgdal)
library(maptools)
library(gdata)

data_newx <- data_newy <- data <- readShapePoly("both.shp")

flip_one = function(x){ # here x is an index into the Large SpatialPolygonsDataFrame
  idx = x
  x = data[x,]
  centroid_x = x@data$INSIDE_X
  centroid_y = x@data$INSIDE_Y
  
  df = data.frame(x@polygons[[1]]@Polygons[[1]]@coords)
  colnames(df) = c("x", "y")
  
  df$x_resid = df$x - centroid_x
  df$y_resid = df$y - centroid_y
  df$new_x = centroid_x - df$x_resid
  df$new_y = centroid_y - df$y_resid
  
  poly_newx = df[,c("new_x", "y")]
  poly_newy = df[,c("x", "new_y")]
  
  poly_orig = df[,c("x", "y")]
  ## However, when I try to fit the new data into the object, it breaks.
  ## I've tried about 20 different things. 
  return(list(poly_newx, poly_newy, poly_orig))
}

alldata = lapply(1:nrow(data), FUN=function(x) data[x,]@data)
alldata = do.call(rbind, alldata)

out = lapply(1:nrow(data), flip_one)
newx = list()
newy = list()
orig = list()
for(i in 1:nrow(data)){
  newx[[i]] = Polygons(list(Polygon(out[[i]][1])), ID=i)
  newy[[i]] = Polygons(list(Polygon(out[[i]][2])), ID=i)
  orig[[i]] = Polygons(list(Polygon(out[[i]][3])), ID=i)
}


spolys_newx = SpatialPolygons(newx, proj4string = CRS("+proj=longlat +datum=WGS84"))
spolys_newy = SpatialPolygons(newy, proj4string = CRS("+proj=longlat +datum=WGS84"))
spolys_orig = SpatialPolygons(orig, proj4string = CRS("+proj=longlat +datum=WGS84"))


rownames(alldata) = as.character(as.numeric(rownames(alldata))+1)

spdf_newx = SpatialPolygonsDataFrame(spolys_newx, alldata)
spdf_newy = SpatialPolygonsDataFrame(spolys_newy, alldata)
spdf_orig = SpatialPolygonsDataFrame(spolys_orig, alldata)


writePolyShape(spdf_newx, fn="both_flipped_x")
writePolyShape(spdf_newy, fn="both_flipped_y")
writePolyShape(spdf_orig, fn="both_orig")
