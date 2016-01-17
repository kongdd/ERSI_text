rm(list = ls())
source('Main_func.R', encoding = 'UTF-8', echo=TRUE)

if (file.exists("data/shp.rda")){
  load("data/shp.rda")
}else{
  WATEA_poly <- readShapePoly("../../merge_param5/WATEA_poly_merge.shp")
  HYDA_poly <- readShapePoly("../../merge_param4/HYDA_poly_merge.shp")
  WATEA_arc <- readShapeLines("../../merge_param5/WATEA_arc_merge.shp")
  HYDL_arc <- readShapeLines("../../merge_param4/HYDL_arc_merge.shp")
  HFCL_arc <- readShapeLines("../../merge_param4/HFCL_arc_merge.shp")
  
  
  shp_poly <- list(HYDA_poly = HYDA_poly, WATEA_poly = WATEA_poly)
  shp_arc <- list(HFCL_arc = HFCL_arc, HYDL_arc = HYDL_arc, WATEA_arc = WATEA_arc)
  save(shp_poly, shp_arc, file = "data/shp.rda")
}
# 面图层处理 -------------------------------------------------------------------

poly_code.unique <- lapply(shp_poly, function(x) sort(unique(x@data$GB)))
guob <- read.xlsx("../../../国标/基础地理信息要素分类与代码(文字版).xlsx", 9)
guob$Name[match(poly_code.unique$HYDA_poly, guob$GB)]
## 866000:似乎是滩涂，对提取水系没有作用
HYDA_poly <- shp_poly[[1]]
HYDA_river = HYDA_poly[HYDA_poly@data$GB %in% poly_code.unique$HYDA_poly[c(1, 8)], ]

# c("常年河", "时令河", "", "时令湖", "水库", "滚水坝", "输水槽", "输水槽", "穴坑")
WATEA_poly <- shp_poly[[2]]
WATEA_river = WATEA_poly[WATEA_poly@data$GB == 6112, ]

# 线图层处理 -------------------------------------------------------------------
arc_code.unique <- lapply(shp_arc, function(x) sort(unique(x@data$GB)))
watea_arc <- shp_arc[[3]]
watea_arc_river <- watea_arc[watea_arc@data$NAME == "乌伦古河", ]
watea_arc_difang <- watea_arc[watea_arc@data$GB == 6462, ]##经判断6462属于提防，提防应该也在河道

## 查看GB编码种类
lapply(shp_arc[1:2], function(x) guob$Name[match(sort(unique(x@data$GB)), guob$GB)])

HFCL_arc <- shp_arc[[1]]
HFCL_arc_difang <- HFCL_arc[HFCL_arc@data$GB == 260400, ]##经判断6462属于提防，提防应该也在河道

# 保存数据 --------------------------------------------------------------------
writePolyShape(HYDA_river, "output/HYDA_poly_river")
writePolyShape(WATEA_river, "output/WATEA_poly_river")
writeLinesShape(watea_arc_difang, "output/watea_arc_difang")
writeLinesShape(HFCL_arc_difang, "output/HFCL_arc_difang")
writeLinesShape(watea_arc_river, "output/watea_arc_river")
