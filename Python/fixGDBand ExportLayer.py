## fix broken layer map， only for floopmapping in xinjiang project
import arcpy
from arcpy import mapping
import os
from os.path import dirname, basename

projectName = u"[05]头屯河"
mxd = mapping.MapDocument("CURRENT")
outdir =  dirname(dirname(mxd.filePath))
gdb_origin = outdir + r"\GBCartoHydroData.gdb".decode("utf-8")
gdb_new = outdir + "\\" + projectName + "_GBCartoHydroData.gdb"

mxd.findAndReplaceWorkspacePaths(gdb_origin, gdb_new)
arcpy.RefreshTOC()

print "===============[After Fixed: Broken layers]=============="
layersBroken = mapping.ListBrokenDataSources(mxd)
for layer in layersBroken: print layer.name

## 导出方案图层
layers = mapping.ListLayers(mxd)
# 记录grouplayer的下标即可
groupLayers = [layer for layer in layers if layer.isGroupLayer and layer.longName.find("\\") == -1]
for layer in groupLayers: print layer.longName
#groupLayers = groupLayers[1:]

for i in range(1, len(groupLayers)):
    layer = groupLayers[i]
    fname = os.path.join(outdir, projectName + "-[" + format(i) + "]" + layer.name + ".lyr")
    print "[%2d]: Writing into %s" % (i, fname)
    layer.saveACopy(fname)

print "Finished"