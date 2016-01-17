rm(list = ls())
## 点图层获取的一定是重点单位
source('Main_func.R', encoding = 'UTF-8', echo=TRUE)

fname = "../../生成数据shp/VEGA_poly.shp"
shp <- readShapePoly(fname)
GB <- sort(unique(shp@data$GB))

guob <- read.xlsx("../../../国标/基础地理信息要素分类与代码(文字版).xlsx", 9)
Names <- guob$Name[match(GB, guob$GB)]
table <- data.frame(GB, Names)##国标和对应类别

shp_out <- shp[shp@data$GB %in% c(9220, 9250, 810302, 810406, 810407), ]
shp_out@data$type = 810300

ColNames <- colnames(shp_out@data)
ColNames[c(13, 17)] <- c("NAME", "type")
colnames(shp_out@data) <- ColNames
writePolyShape(shp_out, "VEGA_poly_out")##生成shapeFile文件
