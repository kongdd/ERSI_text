#coding:utf-8    
#=================-*-coding:utf-8-*-
#Writed by Dongdong Kong, 2015-11-25
import arcpy.mapping as mapping
import arcpy
import os
import re
homedir = 'K:/data'
arcpy.env.workspace = homedir
##添加一个空白的layer group
mxd = mapping.MapDocument("CURRENT")
df = mapping.ListDataFrames(mxd)[0]
VoidLayer = arcpy.mapping.Layer(r"K:/新疆-乌伦古河/ArcGIS_project/VoidLayer.lyr")
VarName1 = ["BOUNT_arc", "BOUNT_point", "BOUNT_poly", "BUILA_poly", "BUILP_arc", "BUILP_point", "NETLN_arc", "OBJLK_point",
"OBJNT_arc", "OBJNT_point", "OBJNT_poly", "PIPLN_arc", "RESPT_point", "ROALK_arc", "TERLK_arc", "TERLK_point",
"TERNT_arc", "TERNT_point", "TERNT_poly", "VEGEA_arc", "VEGEA_poly", "VEGEP_arc", "VEGEP_point", "WATEA_arc",
"WATEA_poly", "WATEP_point", "ROALK_point", "WATEP_arc", "OBJLK_arc"]
## 数据处理操作分为两块,相同要素添加到同一图层
for VarName in VarName1:
	VoidLayer.name = VarName
	arcpy.mapping.AddLayer(df, VoidLayer, "BOTTOM")
	groupLayer = arcpy.mapping.ListLayers(mxd, VarName, df)[0]#group layer
	print VarName
	for fdir in os.listdir(homedir):
		# print fdir#fir only contain directory name, while fpath is fullname
	    # fpath = os.path.join(homedir, fdir)
	    fname = homedir + "/" + fdir + "/" + VarName + ".shp"
	    # 如果该文件实际存在，则把它添加到图层
	    if os.path.isfile(fname):
	    	layer = mapping.Layer(fname)
	    	layer.name = fdir
	        mapping.AddLayerToGroup(df, groupLayer, layer)#添加新的图层
nums = range(len(VarName1) + 1)
k = 0
layers = mapping.ListLayers(mxd)
for i in range(len(layers)):
	if re.search("_", layers[i].name):
		nums[k] = i
		k = k + 1
nums[0] = 0
nums[len(nums) - 1] = len(layers)
print nums
for i in range(len(VarName1)):
	print VarName1[i] + "_merge.shp"#显示进度
	fname = 'K:/新疆-乌伦古河/ArcGIS_project/merge_param5/' + VarName1[i] + "_merge.shp"
	arcpy.Merge_management(layers[(nums[i] + 1):nums[i + 1]], fname)