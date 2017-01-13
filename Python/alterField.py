# -*- coding: utf-8 -*- 
import arcpy
from arcpy import mapping

mxd = mapping.MapDocument("CURRENT")
layers = mapping.ListLayers(mxd)

layer = layers[0]
#field = arcpy.ListFields(layer, "RuleID")
#cursor = arcpy.da.UpdateCursor("domain", ['descript', 'code'])
#for row in cursor:
#    #如果code在domain.codeValues范围内
#    if format(row[0]) in keys:
#        row[1] = domainT[format(row[0])]#row[0]
#    cursor.updateRow(row)

#feature = layer
#field_old = "code"
#field_new = "CODE"
#type = "DOUBLE"
#precision = 10; scale = 2; length = 50;
def alterField(intable, field_old, field_new, type, precision = 10, scale = 2, length = 50, refresh = True):
    # only consider five type variable
    type = type.upper()
    
    funcs = {"DOUBLE":float, "FLOAT":float, "LONG":long, "SHORT":int, "TEXT":str}
    func = funcs[type]

    # if old field name same as new field name, we need a tmp variable
    val = [func(row[0]) for row in arcpy.da.SearchCursor(intable, field_old)]

    # if field name aready exist in original table
    fields = arcpy.ListFields(intable)
    fieldsName = [field.name.upper() for field in fields]
    if field_new.upper() in fieldsName:
        arcpy.DeleteField_management(intable, field_new)

    if type in ["DOUBLE", "FLOAT"]:
        length = None
    elif type in ["LONG", "SHORT"]:
        length = None; scale = None; precision = None
    elif type == "TEXT":
        scale = None; precision = None
        if length == None: length = 50

    arcpy.AddField_management(intable, field_new, type, field_precision = precision, 
                              field_scale = scale, field_length = length) 
    cursor = arcpy.da.UpdateCursor(intable, field_new)
    i = 0;
    for row in cursor:
        row[0] = val[i]; i = i + 1
        cursor.updateRow(row)
    if refresh:
        arcpy.SelectLayerByAttribute_management("转移道路","CLEAR_SELECTION")

# modify field type on batch
def alterFields(intable, fields_old, fields_new, types, precision, scale):
    n = len(fields_old)
    if len(fields_new)!=n or len(types)!=n or len(types)!=n or len(precision)!=n or len(scale)!=n:
        print "parameter error!"
        return
    for i in range(len(fields_old)):
        alterField(intable, fields_old[i], field_new[i], type[i], precision[i], scale[i], length[i], refresh = False)
    arcpy.SelectLayerByAttribute_management("转移道路","CLEAR_SELECTION")
# dbf field types:
# DOUBLE, FLOAT, LONG, SHORT, TEXT, DATE, RASTER, GUID, BLOB

# variable type change functions
# 1 函数                      描述
# 2 int(x [,base ])         将x转换为一个整数
# 3 long(x [,base ])        将x转换为一个长整数
# 4 float(x )               将x转换到一个浮点数
# 5 complex(real [,imag ])  创建一个复数
# 6 str(x )                 将对象 x 转换为字符串
# 7 repr(x )                将对象 x 转换为表达式字符串
# 8 eval(str )              用来计算在字符串中的有效Python表达式,并返回一个对象
# 9 tuple(s )               将序列 s 转换为一个元组
#10 list(s )                将序列 s 转换为一个列表
#11 chr(x )                 将一个整数转换为一个字符
#12 unichr(x )              将一个整数转换为Unicode字符
#13 ord(x )                 将一个字符转换为它的整数值
#14 hex(x )                 将一个整数转换为一个十六进制字符串
#15 oct(x )                 将一个整数转换为一个八进制字符串


#intable = layer
#field_new = "CODE"

#val = [long(row[0]) for row in arcpy.da.SearchCursor(intable, field_old)]
#cursor = arcpy.da.UpdateCursor(intable, field_new)
#i = 0;
#for row in cursor:
#    row[0] = val[i]; i = i + 1
#    cursor.updateRow(row)