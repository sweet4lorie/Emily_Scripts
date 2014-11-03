TITLE = "util"
'''
========================================================================
---->  Nathan Horne's  <----
========================================================================
'''

import xml.etree.ElementTree as xml
from cStringIO import StringIO

import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
import pysideuic
import shiboken

import maya.OpenMayaUI as apiUI

'''
========================================================================
---->  Parse .ui File and Return PySide Class  <----
========================================================================
'''  
def loadUiType(uiFile):
    """
    Pablo Winant
    """
    parsed = xml.parse(uiFile)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text
    
    with open(uiFile, 'r') as f:
        o = StringIO()
        frame = {}
        
        pysideuic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame
        
        form_class = frame['Ui_%s'%form_class]
        base_class = eval('QtGui.%s'%widget_class)
    return form_class, base_class

'''
========================================================================
---->  Get Maya Window  <----
========================================================================
'''  
def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return shiboken.wrapInstance(long(ptr), QtGui.QMainWindow)
