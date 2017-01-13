# 检测数据表中字段是否存在
def existField(feature_class, fieldName, itype = ""):
	flagName = False
	flagType = False
	fields = arcpy.ListFields(feature_class)

	print "%14s %14s %10s %10s %10s %s %s"%("Field", "Alias", "Type", 
		"IsEditable", "Required", "Scale", "precision")
	# Iterate through the list of fields
	for field in fields:
	    # Print field properties
	    print "%14s %14s %10s %10s %10s %3s %3s" % (format(field.name), format(field.aliasName), 
	    	format(field.type), format(field.editable), format(field.required), 
	    	format(field.scale), format(field.precision))
	    if field.name == fieldName:
			flagName = True
			if format(field.type) == itype:
				flagType = True
	if itype == "":flagType = True
	if flagName and flagType:
		print "%s contain %s %s FIELD."%(feature_class, itype, fieldName)
		return True
	else:
		print "%s don't contain %s %s FIELD!"%(feature_class, itype, fieldName)
		return False
# 计算具有平面坐标系统的shapefile area

feature_class = "bou2_4p"
fieldName = "GRIDAREA"
type = "DOUBLE"
unit = "SQUAREMETERS"#SQUAREKILOMETERS

def calculate_Erea(feature_class, fieldName, itype = "Double", unit = "SQUAREMETERS"):
	## 首先需要判断Area Filed是否存在
	fields = arcpy.ListFields(feature_class)
	flag = existField(feature_class, fieldName, itype)

	expression = "float(!SHAPE.area@" + unit + "!)"
	print expression
	if not flag:
		arcpy.AddField_management(feature_class, fieldName, otype.upper())
		arcpy.CalculateField_management(feature_class, fieldName, expression, "PYTHON")

calculate_Erea(feature_class, fieldName)

if field.name.lower() == 'elev':  #look for the name elev
            arcpy.AlterField_management(fc, field, 'ELEVATION', 'Elevation in Metres')