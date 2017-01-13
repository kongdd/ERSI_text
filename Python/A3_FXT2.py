# -*- coding:utf-8 -*-
import sys
import glob
import os, os.path
from os.path import join, basename,dirname
import arcpy.mapping

dont_show = ["测站".decode('utf8')]
working_dir = ''

def get_A3H_lst(path):
    dbf_lst = []
    for root, dirs, files in os.walk(path):
        dbf = [i for i in files if i.decode("cp936") == "A3横.mxd".decode("utf8")]
        for i in dbf:
            dbf_lst.append(join(root,i))
    return dbf_lst
def modify_mxd(mxd_full_path):
    #print("mxd_full_path = %s" %mxd_full_path)
    mxd = arcpy.mapping.MapDocument(mxd_full_path)
    lst = arcpy.mapping.ListDataFrames(mxd)
    #lst[0].scale = 20000000.0
    lst[1].scale = 100000
    #lst[1].elementPositionX = 2.7
    #lst[1].elementPositionY = 2.4
    print (lst[1].scale)

    mxd.save()
    del mxd
def get_pdf_name(mxd_full_path):
    pdf_full_path = os.path.splitext(mxd_full_path)[0] + '.pdf'
    lst = pdf_full_path.split("\\")
    pdf_file_name = "__".join(lst[-3:])
    return pdf_file_name

def hide_cunzhuang(mxd_full_path):
    mxd = arcpy.mapping.MapDocument(mxd_full_path)
    lst = arcpy.mapping.ListDataFrames(mxd)
    layers = arcpy.mapping.ListLayers(mxd,'',lst[1])
    cezhan = []
    global dont_show
    for i in layers:
        if i.name in dont_show:
            i.visible = False
            print(i.name)
    mxd.save()
    del mxd
def mxd2pdf(pdf_path, mxd_full_path):
    mxd = arcpy.mapping.MapDocument(mxd_full_path)
    mxd_file_name = os.path.split(mxd_full_path)[-1]
    mxd_dir_name  = os.path.split(mxd_full_path)[ 0]
    pdf_file_name = os.path.splitext(mxd_file_name)[0] + '.pdf'

    path_lst = mxd_dir_name.split("\\")
    pdf_file_name = path_lst[-2] + "__" + path_lst[-1] + "__" + pdf_file_name

    pdf_full_path = os.path.join(pdf_path, pdf_file_name)
    print (pdf_full_path)
    arcpy.mapping.ExportToPDF(mxd, pdf_full_path)
    del mxd

def mxd2jpeg(jpg_path, mxd_full_path):
    mxd = arcpy.mapping.MapDocument(mxd_full_path)
    mxd_file_name = os.path.split(mxd_full_path)[-1]
    mxd_dir_name  = os.path.split(mxd_full_path)[ 0]
    jpg_file_name = os.path.splitext(mxd_file_name)[0] + '.jpg'

    path_lst = mxd_dir_name.split("\\")
    jpg_file_name = path_lst[-2] + "__" + path_lst[-1] + "__" + jpg_file_name

    jpg_full_path = os.path.join(jpg_path, jpg_file_name)
    print (jpg_full_name)
    arcpy.mapping.ExportToJPEG(mxd, jpg_full_path, resolution=200)
    del mxd


def test0():
    global working_dir
    working_dir = os.getcwd()
    if len(glob.glob('*.frs')) == 0:
        print('请将程序文件放到.frs文件所在的文件夹，程序将退出')
        sys.exit()
    A3_lst = get_A3H_lst(working_dir)
    if len(A3_lst) == 0:
        print('没有找到"A3横.mxd"文件，程序将退出')
        sys.exit()
    if not os.path.exists("pdf"):
        os.mkdir('pdf')
    if not os.path.exists("jpg"):
        os.mkdir('jpg')
    pdf_path =  working_dir + '\\pdf'
    jpg_path =  working_dir + '\\jpg'

    for i in range(len(A3_lst)):
        print(A3_lst[i])
        #modify_mxd(A3_lst[i])
        hide_cunzhuang(A3_lst[i])
        #mxd2jpeg(jpg_path, A3_lst[i])
        mxd2pdf(pdf_path, A3_lst[i])
        print(i)
    sys.exit()
if __name__ == '__main__':
    if sys.version_info.major == 2 and sys.version_info.minor == 7:
        test0()
    else:
        print("运行环境不满足，本程序需要运行于 arcgis Python 2.7，程序即将退出")
