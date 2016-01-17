require(magrittr)
require(openxlsx)

rm(list = ls())
df <- read.xlsx("param4_key_point - 副本.xlsx")

type <- c(320100, 340200, 340101, 340102, 330500, 311100)
type_name <- c("工矿企业", "商贸企业", "学校", "医院", "仓库", "行政机构")

df$type <- type[match(df$type_name, type_name)]
