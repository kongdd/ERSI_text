# help:http://desktop.arcgis.com/zh-cn/arcmap/10.3/analyze/arcpy-data-access/listdomains.htm
def domainPrint(domain):
    print 'Domain name: %s'% domain.name
    if domain.domainType == 'CodedValue':
        coded_values = domain.codedValues
        for val, desc in coded_values.items():
            print '%s: %s'%(format(val), desc)
    elif domain.domainType == 'Range':
        print('Min: {0}'.format(domain.range[0]))
        print('Max: {0}'.format(domain.range[1]))

def updateRuleId(feature, code, ruleId, domain):
    #get representation domain
    keys = domain.codedValues.values()
    domainT = {v:k for k,v in domain.codedValues.items()}#key and value inverse

    cursor = arcpy.da.UpdateCursor(feature, [code, ruleId])
    for row in cursor:
        #如果code在domain.codeValues范围内
        if format(row[0]) in keys:
            row[1] = domainT[format(row[0])]#row[0]
        cursor.updateRow(row)


gdb = r'E:\洪水风险-beijing\洪湖东分块\5地图数据库与图件成果\GBCartoHydroData.gdb'
gdb = r'E:\洪水风险-beijing\洪湖东分块\5地图数据库与图件成果\representation.gdb'
domains = arcpy.da.ListDomains(gdb)
# 获取所有domains
for domain in domains:domainPrint(domain)
# 获取指定名称的domain
domain = [domain for domain in domains if domain.name == u"进水口线_Rep_Rules"][0]
domainPrint(domain)

updateRuleId("进水口线", code = "Code", ruleId = RuleId, domain = domain)