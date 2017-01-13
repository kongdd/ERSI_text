# -*- coding: utf-8 -*- 
__author__ = "Dongdong Kong"
__Date__ = "2016-07-18"
import arcpy
import os

'''
Export shapefile dbf table field property Information to csv files
'''

def existField(feature_class, fieldName, itype = None, show = True, saveFile = True):
    flagName = False
    flagType = False
    fields = arcpy.ListFields(feature_class)

    #print "%14s %14s %10s %10s %10s %s %s" % ("Field", "Alias", "Type", 
    #    "IsEditable", "Required", "Scale", "precision")
    # Iterate through the list of fields
    # show the feature class field information
    colNames = ["Name", "AliasName", "type", "editable", "required", "scale", "precision"]
    fieldInfo = [[format(field.name), format(field.aliasName), format(field.type), format(field.editable), 
      format(field.required), format(field.scale), format(field.precision)] for field in fields]

    # show field information in 
    if show:
        for i in colNames: print "%14s" % i,
        print ""
        for info in fieldInfo:
            for i in info:
                print "%14s" % (i) ,
            print ""

    field = arcpy.ListFields(feature_class, fieldName, itype)
    if itype is None:itype = ""#modified itype value for print in console
    feature = os.path.basename(feature_class)
    
    if len(field) == 0:
        print "%s contain %s %s FIELD." % (feature, itype, fieldName)
        flag = True
    else:
        print "%s don't contain %s %s FIELD!" % (feature, itype, fieldName)
        flag = False

    if saveFile:
        # save fieldInfo into csv file, base on dbf file name if fname is none
        fname = os.path.splitext(feature)[0] + ".csv"
        print fname + u"正在写入..."
        import csv
        writer = csv.writer(open(fname, 'w'), lineterminator='\n')
        writer.writerow(colNames)
        [writer.writerow(r) for r in fieldInfo]
    return flag#true or false

def writeFieldProperty(inputDir, outputDir):
    """
    export table field property batchly
    """
    files = os.listdir(inputDir)
    dbf_files = [os.path.join(inputDir, i) for i in files if os.path.splitext(i)[1] == ".dbf"]

    os.chdir(outputDir)
    print os.getcwd()
    for i in range(len(dbf_files)):
        print "[%02d]------------------------------" % (i + 1)
        existField(dbf_files[i], "VALUE")

inputDir = r"C:\Users\kongdd\Desktop\export"  #dbf table dataIn Table path
outputDir = r"C:\Users\kongdd\Desktop\土地利用".decode("utf-8")#dbf table field information saved path
writeFieldProperty(inputDir, outputDir)
#fname = r"C:\Users\kongdd\Desktop\field.csv"
#import csv
#with open(fname, 'w') as csvfile:
#    writer = csv.writer(csvfile, lineterminator='\n')
#    writer.writerow(colNames)
#    [writer.writerow(r) for r in fieldInfo]

#feature_class = dbf_files[1]
#fields = arcpy.ListFields(feature_class)

## alt + E + V + D????decrease 
##print "%14s %14s %10s %10s %10s %s %s" % ("Field", "Alias", "Type", 
##    "IsEditable", "Required", "Scale", "precision")
## Iterate through the list of fields
## show the feature class field information
#colNames = ["Name", "AliasName", "type", "editable", "required", "scale", "precision"]
#fieldInfo = [[format(field.name), format(field.aliasName), format(field.type), format(field.editable), 
#    format(field.required), format(field.scale), format(field.precision)] for field in fields]
#fieldInfo


#for i in colNames: print "%14s" % i,
#print ""
#for info in fieldInfo:
#    for i in info:
#        print "%14s" % (i) ,
#    print ""