# -*- coding: utf-8 -*-
"""
Created on Thu Jan 05 15:14:00 2017

@author: minyong
"""

import arcpy
import pythonaddins

from mg_ROI_addin import *
import os

type_items = ["plane", "ship","chimney","road","building","car"]
#==============================================================================
# 清空全局变量
#==============================================================================
def mg_clean():
    mg.workspace = ''

    mg.path_image = ''
    mg.path_shp = ''

    mg.just_name_image = ''   # 纯文件名
    mg.just_name_shp = ''     # 纯文件名

    mg.layer_name_image = ''
    mg.layer_name_shp = ''

    mg.features = []

#==============================================================================
#  调试用
#==============================================================================
def mg_showAll():
    print('(workspace) '+ mg.workspace)

    print('(path image) ' + mg.path_image )
    print('(path shape) '+ mg.path_shp)

    print('(just name image) ' + mg.just_name_image )
    print('(just name shp) ' + mg.just_name_shp )

    print('(layer name image) ' + mg.layer_name_image)
    print('(layer name shp) ' + mg.layer_name_shp)


#==============================================================================
# 判断是否有打开的栅格文件，返回找到的第一个图像文件层
# return:
#   layer：打开的文件的层
#   None : 没有打开的栅格文件
#==============================================================================
def raster_has_opened():

    # 判断是否已打开栅格文件
    mxd = arcpy.mapping.MapDocument('CURRENT')      # 当前 mxd
    #layer = arcpy.mapping.ListLayers(mxd)[0]        # 栅格图层

    for layer in arcpy.mapping.ListLayers(mxd):
        if layer.isRasterLayer:
            return layer

    return None


#==============================================================================
# 关闭非 raster 的层
#==============================================================================
def close_not_raster_layer():

    mxd = arcpy.mapping.MapDocument('CURRENT')      # 当前 mxd

    for df in arcpy.mapping.ListDataFrames(mxd):
        for layer in arcpy.mapping.ListLayers(mxd):
            if not layer.isRasterLayer:
                arcpy.mapping.RemoveLayer(df, layer)    # 删除已打开的非图像层


#==============================================================================
# 创建 Shp
# 默认为只存在一个 raster 图层，如果有多个，则加载最后一个
#==============================================================================
def Btn_Create_Shp_OnClick(sup):

    # 判断是否已打开栅格文件
    rasterLayer = raster_has_opened()
    if rasterLayer == None:
        pythonaddins.MessageBox('You must open a raster first!','Error',0)
        return

    # 必须选择有效的文件
    saveFile = pythonaddins.SaveDialog('Save Shp File to',
                                        rasterLayer.name.split('.')[0] + '.shp')
    if saveFile == None:
        print('__[MG]__:Shape file not created!')
        return

    # 必须为新文件
    if os.path.isfile(saveFile):
        pythonaddins.MessageBox('Shape file already exists!','Error',0)
        return

    # 必须为 Shp 文件
    suffix = saveFile.split('.')[1]
    if suffix != 'Shp' and suffix != 'shp':
        pythonaddins.MessageBox('Must choose a Shape file!','Error',0)
        return

    # 关闭非图像层
    close_not_raster_layer()

    mg_clean()      # 清空全局变量

    # 得到全局各种变量
    mg.layer_image = rasterLayer
    mg.layer_name_image = rasterLayer.name
    mg.just_name_image = rasterLayer.name.split('.')[0]
    mg.path_image = rasterLayer.dataSource

    mg.path_shp   = saveFile
    mg.just_name_shp = os.path.split(saveFile)[1].split('.')[0]
    mg.layer_name_shp = mg.just_name_shp

    mg.workspace  = os.path.split(saveFile)[0]    # 文件夹路径

    # 更改workspace
    print('__[MG]__: change workspace to ' + mg.workspace + '......')
    arcpy.env.workspace = mg.workspace
    print('__[MG]__: Done!')

    # 创建 Shp
    print('__[MG]__:Create Shp file ' + saveFile)
    arcpy.CreateFeatureclass_management(mg.workspace,
                                        mg.just_name_shp + '.shp',
                                        "POLYLINE")
    arcpy.AddField_management(saveFile,"Type",'TEXT')   # 创建目标类型的 field
    print('__[MG]__: Done!')

    # 找到这个 layer
    mxd = arcpy.mapping.MapDocument('CURRENT')      # 当前 mxd
    for layer in arcpy.mapping.ListLayers(mxd):
        if layer.name == mg.just_name_shp:
            mg.layer_shp = layer

    arcpy.RefreshActiveView()
    arcpy.RefreshTOC()

    #mg_showAll()

#==============================================================================
# 打开 Shp
#==============================================================================
def Btn_Open_Shp_OnClick(sup):

    # 判断是否已打开栅格文件
    rasterLayer = raster_has_opened()
    if rasterLayer == None:
        pythonaddins.MessageBox('You must open a raster first!','Error',0)
        return

    # 必须选择有效的文件
    openFile = pythonaddins.OpenDialog('Choose the Shp File',False,'./')
    if openFile == None:
        print('__[MG]__: Shp file: not change')
        return

    # 必须为 Shp 文件
    suffix = openFile.split('.')[1]
    if suffix != 'Shp' and suffix != 'shp':
        pythonaddins.MessageBox('Must choose a Shp file!','Error',0)
        return

    # 关闭非图像层
    close_not_raster_layer()

    mg_clean()      # 清空全局变量

    # 得到全局各种变量
    mg.layer_image = rasterLayer
    mg.layer_name_image = rasterLayer.name
    mg.just_name_image = rasterLayer.name.split('.')[0]
    mg.path_image = rasterLayer.dataSource

    mg.path_shp   = openFile
    mg.just_name_shp = os.path.split(openFile)[1].split('.')[0]
    mg.layer_name_shp = mg.just_name_shp

    mg.workspace  = os.path.split(openFile)[0]    # 文件夹路径


    # 更改workspace
    print('__[MG]__: change workspace to ' + mg.workspace + '......')
    arcpy.env.workspace = mg.workspace
    print('__[MG]__: Done!')

    # 加载 shp 文件
    print('__[MG]__: Loading shp ......')
    mxd = arcpy.mapping.MapDocument("CURRENT")      # 获得当前的document
    df = arcpy.mapping.ListDataFrames(mxd,"*")[0]   # 获得 data frame
    mg.layer_shp = arcpy.mapping.Layer(mg.path_shp)      # 创建新图层
    arcpy.mapping.AddLayer(df, mg.layer_shp,"TOP")      # 添加图层，放到最下面
    print('__[MG]__: Done!')

    arcpy.RefreshActiveView()
    arcpy.RefreshTOC()

    #mg_showAll()

#==============================================================================
# 打开 Txt
#==============================================================================
def Btn_Open_Txt_OnClick(sup):

    # 判断是否已打开栅格文件
    rasterLayer = raster_has_opened()
    if rasterLayer == None:
        pythonaddins.MessageBox('You must open a raster first!','Error',0)
        return

    # 选择必须有效
    txtFile = pythonaddins.OpenDialog('Choose the Txt File',False,'./')
    if txtFile == None:
        print('__[MG]__: Shp file: not change')
        return

    # 必须为 Txt 文件
    suffix = txtFile.split('.')[1]
    if suffix != 'txt':
        pythonaddins.MessageBox('Must choose a Txt file!','Error',0)
        return

    # 关闭非图像层
    close_not_raster_layer()

    mg_clean()      # 清空全局变量

    # 得到全局各种变量
    mg.layer_image = rasterLayer
    mg.layer_name_image = rasterLayer.name
    mg.just_name_image = rasterLayer.name.split('.')[0]
    mg.path_image = rasterLayer.dataSource

    mg.path_shp   = txtFile.split('.')[0] + '.shp'
    mg.just_name_shp = os.path.split(txtFile)[1].split('.')[0]
    mg.layer_name_shp = mg.just_name_shp

    mg.workspace  = os.path.split(txtFile)[0]    # 文件夹路径

#    print txtFile
#    mg_showAll()
#    return

    # 更改workspace
    print('__[MG]__: change workspace to ' + mg.workspace + '......')
    arcpy.env.workspace = mg.workspace
    print('__[MG]__: Done!')

    # 创建 Shp
    print('__[MG]__:Create Shp file ' + txtFile)
    arcpy.CreateFeatureclass_management(mg.workspace,
                                        mg.just_name_shp + '.shp',
                                        "POLYLINE")
    arcpy.AddField_management(mg.path_shp,"Type",'TEXT')   # 创建目标类型的 field
    print('__[MG]__: Done!')

    # 找到这个 layer
    mxd = arcpy.mapping.MapDocument('CURRENT')      # 当前 mxd
    for layer in arcpy.mapping.ListLayers(mxd):
        if layer.name == mg.just_name_shp:
            mg.layer_shp = layer

    # 读入 Txt 里面的坐标，每行加一个矩形
    with open(txtFile,'r') as f:
        for line in f:
            tmplist = line.split(',')
            #print tmplist
            [p1x,p1y,p2x,p2y] = list(map(float,tmplist[:-1]))
            tp = tmplist[-1]
            print p1x,p1y,p2x,p2y,tp

            rows = arcpy.InsertCursor(mg.path_shp)
            rect = arcpy.Array([arcpy.Point(p1x,p1y),
                                arcpy.Point(p2x,p1y),
                                arcpy.Point(p2x,p2y),
                                arcpy.Point(p1x,p2y),
                                arcpy.Point(p1x,p1y)])
            ROI = arcpy.Polyline(rect)

            row = rows.newRow()
            row.setValue('Shape',ROI)
            row.setValue('Type',tp)
            rows.insertRow(row)

    print('__[MG]__: new shp created!')

    # 加载 shp 文件
#    print('__[MG]__: Loading shp ......')
#    mxd = arcpy.mapping.MapDocument("CURRENT")      # 获得当前的document
#    df = arcpy.mapping.ListDataFrames(mxd,"*")[0]   # 获得 data frame
#    mg.layer_shp = arcpy.mapping.Layer(mg.path_shp)      # 创建新图层
#    arcpy.mapping.AddLayer(df, mg.layer_shp,"TOP")      # 添加图层，放到最下面
#    print('__[MG]__: Done!')

    arcpy.RefreshActiveView()


    #mg_showAll()


#==============================================================================
# 更改 enable
#==============================================================================
def Btn_ChooseEnable_OnClick(sup):
    if tool_ROI.enabled == True:
        tool_ROI.enabled = False
        print('__[MG]__: choose ROI is disabled!')
    else:
        tool_ROI.enabled = True
        print('__[MG]__: choose ROI is enabled!')


#==============================================================================
# 删除
#==============================================================================
def Btn_Delete_OnClick(sup):
    '删除选择的子 ROI，每删除一个都要确认'

    # 判断是否已打开栅格文件
    rasterLayer = raster_has_opened()
    if rasterLayer == None:
        pythonaddins.MessageBox('You must open a raster first!','Error',0)
        return

    with arcpy.da.UpdateCursor(mg.layer_name_shp,'*') as cursor:
        for row in cursor:
            ansDel = pythonaddins.MessageBox('Delete FID: '+ str(row[0]),
                                             'Confirm delete', 3)
            if ansDel == 'Yes':
                cursor.deleteRow()
                arcpy.RefreshActiveView()
            elif ansDel == 'No':
                continue
            else:
                return


#==============================================================================
#     保存为 txt
#==============================================================================
def Btn_SaveTxt_OnClick(sup):
    '把选中的 feature 的坐标范围保存到指定 txt 文件'

    # 判断是否已打开栅格文件
    rasterLayer = raster_has_opened()
    if rasterLayer == None:
        pythonaddins.MessageBox('You must open a raster first!','Error',0)
        return

    saveTxt = pythonaddins.SaveDialog('Choose the save file',
                                       mg.just_name_shp +'.txt')
    #print saveTxt
    if saveTxt == None:
        print 'cancel'
        return


    # 写文本
    with open(saveTxt,'w') as f:
        cursor = arcpy.UpdateCursor(mg.layer_shp)
        for row in cursor:
            tp = row.getValue('TYPE')
            geom = row.getValue('SHAPE')
            #print type(geom)
            array = geom.getPart(0)
            listX = []
            listY = []


            for x in range(1,array.count):
                listX.append(array[x].X)
                listY.append(array[x].Y)


            f.write('%f,%f,%f,%f,%s\n' % ( min(listX), min(listY),
                          max(listX), max(listY), tp ))

            print('__[MG]__:\n p1:(%f,%f) \n p2:(%f,%f) \n type: %s' % (min(listX), min(listY), max(listX), max(listY), tp))

    print('\n__[MG]__: Save points to ' + saveTxt)


#==============================================================================
#  处理函数
#==============================================================================
def Btn_Process_OnClick(sup):
    '打开points 文件，把各子区域保存为 jpg 图片'
#    arcpy.Point(223469.975728 3352836.06796)
#    223624.830097 3352993.59223
#    img=arcpy.RasterToNumPyArray(mg.path_image, arcpy.Point(223424,3353087),10,10)

    ######################
    chosenFile = pythonaddins.OpenDialog('Choose the ROI Points File',False,'./')
    if chosenFile == None:
        return

    with open(chosenFile,'r') as f:
        num = 0
        for line in f:
#            minX,minY,maxX,maxY = [ float(x) for x in line.strip().split(',') ]
#            #print type(minX)
#            print minX,minY,maxX,maxY

            tmplist = line.split(',')
            #print tmplist
            [minX,minY,maxX,maxY] = list(map(float,tmplist[:-1]))
            tp = tmplist[-1]
            print minX,minY,maxX,maxY,tp

            numpyImg = arcpy.RasterToNumPyArray(mg.path_image,
                                           arcpy.Point(minX,minY),
                                           int(maxX-minX),int(maxY-minY))
            rasterImg = arcpy.NumPyArrayToRaster(numpyImg)
            num += 1
            arcpy.MakeRasterLayer_management(rasterImg,'Img'+str(num))
            rasterImg.save(mg.workspace + '/Img' + str(num) + '.tif')

    print('Done!')
    arcpy.RefreshActiveView()
    arcpy.RefreshTOC()


#==============================================================================
#
#==============================================================================
def Tool_ROI_onMouseDown(sup, x, y, button, shift):
    #
    if button == 2:
        print 'down: ','x: ',x,' , y:',y
    pass


#==============================================================================
#
#==============================================================================
def Tool_ROI_onMouseDownMap(sup, x, y, button, shift):

    if button == 2:
        print 'map: ','x: ',x,' , y:',y
    pass

#==============================================================================
# 选择 ROI
#==============================================================================
def Tool_ROI_OnRectangle(sup,rectangle_geometry):

    rows = arcpy.InsertCursor(mg.path_shp)

    ext = rectangle_geometry
    rect = arcpy.Array([ext.lowerLeft, ext.lowerRight,
                        ext.upperRight,  ext.upperLeft, ext.lowerLeft])
    ROI = arcpy.Polyline(rect)
    #thepoly = arcpy.Polygon(,df.spatialReference)

    row = rows.newRow()
    row.setValue('Shape',ROI)
    row.setValue('Type',str(combobox_type.value))
    rows.insertRow(row)

    tool_ROI.enabled = False  # 保证每次只选一个

    arcpy.RefreshActiveView()
    print('__[MG]__: new ROI inserted!')


#==============================================================================
# About
#==============================================================================
def Btn_About_OnClick(sup):
    pythonaddins.MessageBox('image:\t' + mg.path_image + '\n' +
                            'shp:\t' + mg.path_shp + '\n' +
                            'outupt:',
                            'Information')
