rm(list = ls())
## 点图层获取的一定是重点单位
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

source('Main_func.R', encoding = 'UTF-8', echo=TRUE)
#   CGCS2000 / 3-degree Gauss-Kruger zone 29, 
#   +proj=tmerc +lat_0=0 +lon_0=87 +k=1 +x_0=29500000 +y_0=0 +ellps=GRS80 +units=m +no_defs
fnames <- dir("../../merge_param4/", pattern = "*point_merge.shp$", full.names = T)
Names <- dir("../../merge_param4/", pattern = "*point_merge.shp$")

delFile = c(2, 3, 4, 5, 6, 8, 9)
fnames <- fnames[-delFile]
Names <- Names[-delFile]

df_list <- lapply(fnames, get_shpdata) %>% set_names(substr(Names, 1, 10))
# shp_write.xlsx2("param4_point.xlsx", df_list)
## 通过param4_point.xlsx文件可以准确判断，HFCP, PIPP, RESP, VEGES不含重点单位
# df_list <- df_list[]

shp_code.unique <- lapply(df_list, function(x) unique(x$GB))
## meanwhile save longitude and latitude information
# df <- melt(df_list, id.vars = c("long", "lat", "GB", "Name", "type"))
df_trim <- lapply(df_list, function(x) x[, c("long", "lat", "AREA", "PERIMETER", "GB", "NAME")])
df <- melt(df_trim, id.vars = colnames(df_trim[[1]]))

## 输出数据根据国标编号进行排序
df_new <- df[sort(df$GB, index.return = T)$ix, ]

guob <- read.xlsx("../../../国标/基础地理信息要素分类与代码(文字版).xlsx", 9)
df_new$GB_name <- guob$Name[match(df_new$GB, guob$GB)]

write.xlsx(df_new, file = "param4_key_point.xlsx")
