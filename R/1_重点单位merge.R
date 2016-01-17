rm(list = ls())
source('Main_func.R', encoding = 'UTF-8', echo=TRUE)

fnames <- dir("../../福海县重点单位/CGCS2000/", pattern = "*.shp$", full.names = T)
Names <- c("大厦", "购物", "金融服务", "科研教育", "休闲娱乐", "医疗服务", "政府机关")
code =  c(340200, 340200, 340200, 340101, 330500, 340102, 311100)

shape <- lapply(fnames, function(x) readShapePoints(x)) %>% set_names(Names)

shape <- lapply(fnames, function(x) readShapePoints(x))
latlong <- lapply(shape, function(x) { ans <- data.frame(coordinates(x)); colnames(ans) <- c("long", "lat"); ans})
df <- lapply(shape, function(x) x@data[, c("NAME", "MAPID", "KIND","ADDRESS")])

N <- length(fnames)
df_out <- list()
for(i in 1:N){
  df_out[[i]] <- cbind(latlong[[i]], df[[i]])
}
names(df_out) <- Names
df_points <- melt(df_out, id.vars = c("long","lat", "NAME", "MAPID", "KIND","ADDRESS")) %>% 
  set_colnames(c(colnames(.)[-ncol(.)], "type_name"))
df_points$type <- code[match(df_points$type, Names)]
coordinates(df_points) <- ~long + lat
proj4string(df_points) <- proj_g

## 直接转化为我们需要的类型
#  类型编码用于区分重点单位类型，如：320100 表示工矿企业，
#  340200表示商贸企业，340101表示学校，340102表示医院，330500表示仓库，311100表示行政机构。
#  大厦、购物、金融服务定义为商贸企业，休闲娱乐定义为仓库
# writeOGR(df_points, "output", "KeyPoints_merge", driver="ESRI Shapefile", overwrite_layer = T)
writePointsShape(df_points, "output/KeyPoints_merge")