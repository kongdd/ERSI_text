library(magrittr)
library(foreign)
library(plyr)

## 属性表table字段信息获取采用python进行，字段修改采用R语言处理

source("MainFunc_AlterField.R", encoding = "UTF-8")
# precisionIn: filed length，should be caution that: number of digits including minus sign and decimal sign
# scaleIn: digits after the decimal sign
# copyfile: if TRUE, 原始dbf在进行操作时首先进行备份，文件名修改为"*.dbfold"

## -----------global functions-----------
inputDir <- "C:/Users/kongdd/Desktop/export"
# files <- dir(inputDir, pattern = "*.shp$")
# fileNames <- gsub(".shp", "", files)
filepaths <- dir(inputDir, pattern = "*.dbf$", full.names = T)

## 对dbf的数据框进行修改
df <- read.dbf(filepaths[2])
VALUE = round(df[, 1], 3)
# names(df) <- gsub(".dbf", "", basename(filepaths))
df_new <- data.frame(GRIDCODE = as.double(seq_along(VALUE)), VALUE, author = "崔俭俭")
writeDBF(df_new, filepaths[1], precisionIn = c(10, 10, 10) + 1, scaleIn = c(0, 3, 0), copyfile = T)
