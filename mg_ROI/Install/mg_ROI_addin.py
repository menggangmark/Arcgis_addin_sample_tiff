# -*- coding: utf-8 -*-
"""
Created on Thu Jan 05 15:14:00 2017

@author: minyong
"""
import arcpy
import pythonaddins

#==============================================================================
# 用于调试
#==============================================================================
import sys
sys.path.append('E:/ArcGIS_python/mg_arcpy/mg_ROI/Install')
from imp import reload
import mg_Funcs

#==============================================================================
# 全局变量
#==============================================================================

class mg:

    workspace = ''

    path_image = ''         # 可以去掉
    path_shp = ''           # 可以去掉

    just_name_image = ''    # 纯文件名
    just_name_shp = ''      # 纯文件名

    layer_name_image = ''   # 可以去掉
    layer_name_shp = ''     # 可以去掉

    layer_image = None
    layer_shp = None

    features = []           # 可以去掉


#==============================================================================
#  创建 Shp
#==============================================================================
class ButtonClass_CreateShp(object):
    """Implementation for mg_ROI_addin.button_create_shp (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        reload(mg_Funcs)
        mg_Funcs.Btn_Create_Shp_OnClick(self)


#==============================================================================
# 打开 Shp
#==============================================================================
class ButtonClass_OpenShp(object):
    """Implementation for mg_ROI_addin.button_open_shp (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        reload(mg_Funcs)
        mg_Funcs.Btn_Open_Shp_OnClick(self)


#==============================================================================
# 打开Txt
#==============================================================================
class ButtonClass_OpenTxt(object):
    """Implementation for mg_ROI_addin.button_open_txt (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        reload(mg_Funcs)
        mg_Funcs.Btn_Open_Txt_OnClick(self)


#==============================================================================
# 保存 Txt
#==============================================================================
class ButtonClass_SaveTxt(object):
    """Implementation for mg_ROI_addin.button_save_txt (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        reload(mg_Funcs)
        mg_Funcs.Btn_SaveTxt_OnClick(self)


#==============================================================================
# Enable
#==============================================================================
class ButtonClass_ChooseEnable(object):
    """Implementation for mg_ROI_addin.button_choose_enable (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        reload(mg_Funcs)
        mg_Funcs.Btn_ChooseEnable_OnClick(self)

#==============================================================================
# 删除 ROI
#==============================================================================
class ButtonClass_Delete(object):
    """Implementation for mg_ROI_addin.button_delete (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        reload(mg_Funcs)
        mg_Funcs.Btn_Delete_OnClick(self)



#==============================================================================
# 处理测试函数
#==============================================================================
class ButtonClass_Process(object):
    """Implementation for mg_ROI_addin.button_process (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        reload(mg_Funcs)
        mg_Funcs.Btn_Process_OnClick(self)


#==============================================================================
# 坐标系选择
#==============================================================================
class ComboBoxClass_Type(object):
    """Implementation for mg_ROI_addin.combobox_coor (ComboBox)"""
    def __init__(self):
        self.items = mg_Funcs.type_items
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWW'
        self.width = 'WWWWW'
        self.value = self.items[0]
    def onSelChange(self, selection):
        pass
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        pass
    def onEnter(self):
        pass
    def refresh(self):
        pass


#==============================================================================
# Tool
#==============================================================================
class ToolClass_ROI(object):
    """Implementation for mg_ROI_addin.tool_ROI (Tool)"""
    def __init__(self):
        self.enabled = True
        #self.shape = "NONE" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.
        self.shape = "Rectangle"
    def onMouseDown(self, x, y, button, shift):
        reload(mg_Funcs)
        mg_Funcs.Tool_ROI_onMouseDown(self, x, y, button, shift)

    def onMouseDownMap(self, x, y, button, shift):
        reload(mg_Funcs)
        mg_Funcs.Tool_ROI_onMouseDownMap(self, x, y, button, shift)

    def onMouseUp(self, x, y, button, shift):
        pass
    def onMouseUpMap(self, x, y, button, shift):
        pass
    def onMouseMove(self, x, y, button, shift):
        pass
    def onMouseMoveMap(self, x, y, button, shift):
        pass
    def onDblClick(self):
        pass
    def onKeyDown(self, keycode, shift):
        pass
    def onKeyUp(self, keycode, shift):
        pass
    def deactivate(self):
        pass
    def onCircle(self, circle_geometry):
        pass
    def onLine(self, line_geometry):
        pass
    def onRectangle(self, rectangle_geometry):
        reload(mg_Funcs)
        mg_Funcs.Tool_ROI_OnRectangle(self, rectangle_geometry)


#==============================================================================
# About
#==============================================================================
class ButtonClass_About(object):
    """Implementation for mg_ROI_addin.button_about (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        reload(mg_Funcs)
        mg_Funcs.Btn_About_OnClick(self)