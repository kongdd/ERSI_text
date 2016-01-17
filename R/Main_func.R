require(maptools)
require(lattice)
require(plyr)
require(magrittr)
require(snow)
require(openxlsx)
require(rgdal)
require(reshape2)

# 数据统一采用同一大地坐标系统进行处理
#   CGCS2000 / 3-degree Gauss-Kruger zone 29, 
#   +proj=tmerc +lat_0=0 +lon_0=87 +k=1 +x_0=29500000 +y_0=0 +ellps=GRS80 +units=m +no_defs
proj_g <- CRS("+init=epsg:4517")

#   China Geodetic Coordinate System 2000
#   +proj=longlat +ellps=GRS80 +no_defs
proj_p <- CRS("+init=epsg:4490")
## 如果大地坐标系统不对的话，对大地坐标系统就行定义调整
proj_transform <- function(shp){
  if (is.na(proj4string(shp))){
    bbox_range <- shp@bbox
    range <- aaply(bbox_range, 1, diff)
    
    if (max(bbox_range) < 1000){#说明该大地坐标系统是 经纬度型
      proj4string(shp) <- proj_p
      shp <- spTransform(shp, proj_g)
    }else{
      proj4string(shp) <- proj_g
    }
  }
  shp
}

## 判断大地坐标系统异常的layer
## 如果大地坐标系统不对的话，对大地坐标系统就行定义调整
get_proj <- function(shp){
  if (is.na(proj4string(shp))){
    bbox_range <- shp@bbox
    range <- aaply(bbox_range, 1, diff)
    
    if (max(bbox_range) < 1000){#说明该大地坐标系统是 经纬度型
      proj_p
    }else{
      proj_g
    }
  }
}

get_typeId <- function(typei){
  out <- which(laply(types, function(x) typei %in% x))
  if(length(out) == 0) out <- NA
  out
} 

# 处理要素说明 ------------------------------------------------------------------

#   去掉：BOU, TER
#   植被VEG
#   水系HYD, HFC, WAT
#   建筑：BUI, RFC, RES, OBJ
types <- list()
types[[1]] <- "VEG"
types[[2]] <- c("HYD", "HFC", "WAT")
types[[3]] <- c("BUI", "RFC", "RES", "OBJ")
# 分为三层
# zaol <- c(19, 28.57, 18.18)

get_gridNAs <- function(fpath, fname){
  # 生成空栅格数据图层 ---------------------------------------------------------------
  
  fname_grid <- sprintf("%s/%s", fpath, fname[which(substr(fname, 1, 3) == "VEG")])
  # fname_grid <- "../11/L45G021054/VEGEA_poly.shp"
  shape <- readShapePoly(fname_grid)
  shape <- proj_transform(shape)#如果大地坐标系统为NA或者大地坐标系
  
  bbox_range <- shape@bbox
  # bbox_range
  ##优化程序结构确保拼接的时候不会出错,可以保证边界都是整数
  bbox_range[, 1] <- bbox_range[, 1] %>% aaply(., 1, function(x) x - (x %% 20))
  bbox_range[, 2] <- bbox_range[, 2] %>% aaply(., 1, function(x) x - (x %% 20) + 20)
  # bbox_range
  
  range <- aaply(bbox_range, 1, diff)
  
  cellsize <- 20
  celldim <- floor(range/cellsize)
  
  grid <- GridTopology(cellcentre.offset = bbox_range[, 1] + cellsize/2, 
                       cellsize = c(1, 1) * cellsize, cells.dim = celldim)
  grid <- SpatialPixelsDataFrame(grid, data = data.frame(id = 1:prod(celldim)))
  grid@data <- grid@data * NA
  proj4string(grid) <- proj_g
  grid#quickly return
}

## 获取最终的栅格范围
get_gridNAs_Big <- function(result){
  bound <- sapply(result, function(x) x@bbox) %>% matrix(., length(.)/4, 4, byrow = T)
  
  l_bound <- c(aaply(bound, 2, min)[1:2]) %>% aaply(., 1, function(x) x - (x %% 20))
  u_bound <- c(aaply(bound, 2, max)[3:4]) %>% aaply(., 1, function(x) x - (x %% 20) + 20)
  
  bbox_rangeO <- matrix(c(aaply(bound, 2, min)[1:2], aaply(bound, 2, max)[3:4]), 2)
  bbox_range <- matrix(c(l_bound, u_bound), 2)
  range <- aaply(bbox_range, 1, diff)
  
  cellsize <- 20
  celldim <- floor(range/cellsize)
  
  grid <- GridTopology(cellcentre.offset = bbox_range[, 1] + cellsize/2, 
                       cellsize = c(1, 1) * cellsize, cells.dim = celldim)
  grid <- SpatialPixelsDataFrame(grid, data = data.frame(id = 1:prod(celldim)))
  grid@data <- grid@data * NA
  proj4string(grid) <- proj_g
  grid
}

#为并行运算所准备
get_landuse_OnePiece <- function(i, fpaths){
    setTxtProgressBar(pb, i)
    
    fpath <- fpaths[i]
    fname <- dir(fpath, pattern = ".*_poly.shp$")
    ftype <- as.character(aaply(fname, 1, function(type) substr(type, 1, 3)))
    ftypeId <- aaply(ftype, 1, get_typeId)
    
    grid <- get_gridNAs(fpath, fname)
    
    zaol <- c(19, 28.57, 18.18)
    for (j in 1:3){
      Id <- which(ftypeId == j)
      if (length(Id) > 0){
        for (k in seq_along(Id)){
          
          fname_j <- sprintf("%s/%s", fpath, fname[k])
          # fname_j <- "./L45G021054/BUILA_poly.shp"
          shape <- readShapePoly(fname_j)
          shape <- proj_transform(shape)#如果大地坐标系统为NA或者大地坐标系
          
          Id_shape <- over(grid, shape[, 1]); id_shape <- which(!is.na(Id_shape))
          grid@data[id_shape, ] <- zaol[j]
        }
      }
    }
    ## 这样进行数据拼接运算速度非常慢
    grid
}

## 保存矢量文件的table数据
shp_write.xlsx <- function(fpath, fname, x){
  wb <- createWorkbook()
  options("openxlsx.borderStyle" = "none")
  # options("openxlsx.borderColour" = "#4F81BD")
  hs1 <- createStyle(fgFill = "#DCE6F1", halign = "CENTER", textDecoration = "Italic",
                     border = "Bottom")
  ## Add worksheets
  for (i in seq_along(fname)){
    addWorksheet(wb, fname[i])
    
    writeData(wb, fname[i], x[[i]], colNames = TRUE, rowNames = TRUE, borders="rows", 
              headerStyle = hs1)
  }
  saveWorkbook(wb, paste(substr(fpath, 6, 15), ".xlsx", sep = ""), overwrite = TRUE)
}

## 保存矢量文件的table数据
shp_write.xlsx2 <- function(fileName, x){
  ## x,是一个list data
  wb <- createWorkbook()
  options("openxlsx.borderStyle" = "none")
  # options("openxlsx.borderColour" = "#4F81BD")
  hs1 <- createStyle(fgFill = "#DCE6F1", halign = "CENTER", textDecoration = "Italic",
                     border = "Bottom")
  fname <- names(x)
  ## Add worksheets
  for (i in seq_along(fname)){
    addWorksheet(wb, fname[i])
    
    writeData(wb, fname[i], x[[i]], colNames = TRUE, rowNames = TRUE, borders="rows", 
              headerStyle = hs1)
  }
  saveWorkbook(wb, fileName, overwrite = TRUE)
}

## function get shape file according file names
## 同时获取精度纬度，方便对数据进行融合
#' @param type only can be 'Points', 'Lines' or 'Poly'
get_shpdata <- function(fname, type = "Points"){
  if (type %in% c("Points", "Lines", "Poly")){
    fun <- getFunction(paste("readShape", type, sep = ""))
    shp <- fun(fname)
    latlong <- coordinates(shp) %>% set_colnames(c("long", "lat"))
    cbind(latlong, shp@data)##return result
  }else{
    warning("The parameter 'type' input is error!")
  }
}