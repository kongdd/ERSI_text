from arcpy import mapping
mxd = mapping.MapDocument("CURRENT")
layers = mapping.ListLayers(mxd)
layers = [layer for layer in layers if not layer.isGroupLayer]
def get_tableCount(layer):
	n = 0
	# Create the search cursor
	cursor = arcpy.SearchCursor(layer.longName)
	# Iterate through the rows in the cursor
	for row in cursor: n = n + 1
	return(n)

df = arcpy.mapping.ListDataFrames(mxd)[0]
for layer in layers:
    # if layer.name.find("Anno") != -1: continue
    if layer.longName.find(u"水利工程") == -1: break
    if get_tableCount(layer) == 0: 
        print layer.longName
        arcpy.mapping.RemoveLayer(df, layer)