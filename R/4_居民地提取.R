rm(list = ls())
source('Main_func.R', encoding = 'UTF-8', echo=TRUE)

fname = "../../洪水风险评估-data/RESA_poly.shp"

shp <- readShapePoly(fname)
GB <- sort(unique(shp@data$GB))

guob <- read.xlsx("../../../国标/基础地理信息要素分类与代码(文字版).xlsx", 9)
Names <- guob$Name[match(GB, guob$GB)]
Names[1:4] <- c("一般房屋", "破坏房屋", "地面不能住人窑洞", "坑穴")

table <- data.frame(GB, Names)
# write.xlsx(table, file = "4_居民地table.xlsx")

table <- read.xlsx("data/4_居民地table.xlsx")
table <- table[which(!is.na(table$type_name)), ]##仅保留可以辨别的居民地类型

shp_out <- shp[shp@data$GB %in% table$GB, ]
data_in <- shp_out@data[, c(1:7, 16:17)]
data_in$type_name <- table$type_name[match(data_in$GB, table$GB)]
type <- c(310100, 310200)
data_in$type <- factor(type[match(data_in$type_name, c("农村居民地", "城镇居民地"))])

shp_out@data <- data_in
writePolyShape(shp_out, "RESA_poly")##生成shapeFile文件
write.xlsx(data_in, file = "resa.xlsx")##导出属性表