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
VarName2 = ["AANP_point", "BOUA_poly", "CPTL_arc", "HFCP_point", "HYDA_poly", "HYDL_arc", "HYDP_point", "RESP_point",
"TERL_arc", "TERP_point", "VEGA_poly", "VEGL_arc", "HFCL_arc", "LFCL_arc", "LFCP_point", "PIPL_arc", 
"RESA_poly", "RESL_arc", "RFCA_poly", "RFCL_arc", "TERA_poly", "VEGP_point", "RFCP_point", "PIPP_point", "HFCA_poly"]
## 数据处理操作分为两块,相同要素添加到同一图层
for VarName in VarName2:
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
nums = range(len(VarName2) + 1)
k = 0
layers = mapping.ListLayers(mxd)
for i in range(len(layers)):
	if re.search("_", layers[i].name):
		nums[k] = i
		k = k + 1
nums[0] = 0
nums[len(nums) - 1] = len(layers)
print nums
for i in range(len(VarName2)):
	print VarName2[i] + "_merge.shp"
	fname = 'K:/新疆-乌伦古河/ArcGIS_project/merge_param4/' + VarName2[i] + "_merge.shp"
	arcpy.Merge_management(layers[(nums[i] + 1):nums[i + 1]], fname)