TITLE = "Name Helper"
DESCRIPTION = "Helps rename selected objects."
IMAGE = "commandButton.png"
RUN_COMMAND = "import NameHelper as nh; reload(nh); nh.main();"
ICON_LABEL = "Name"

import os
import maya.cmds as cmds
import PySideUtil as psUtil
reload(psUtil)
from functools import partial

thisdirectory = os.path.dirname(os.path.realpath(__file__))
uiFile = os.path.join(thisdirectory, "ui", "NameHelper.ui")
form_class, base_class = psUtil.loadUiType(uiFile)


class NameHelper(base_class, form_class):
    def __init__(self, parent = psUtil.getMayaWindow()):
        super(NameHelper, self).__init__(parent)
        self.setupUi(self)
        self.connectUi()


    def connectUi(self):
        self.suffixAddButton.pressed.connect(partial(self.suffix, "add"))
        self.suffixRemoveButton.pressed.connect(partial(self.suffix, "delete"))
        self.renameButton.pressed.connect(self.rename)
        self.numerateButton.pressed.connect(self.numberate)


    def suffix(self, typeStr):
        suffixStr = "_" + (self.suffixComboBox.currentText()).__str__()
        sList = cmds.ls(selection = True)
        for s in sList:
            if typeStr == "add":
                cmds.rename(s, s + suffixStr)
            elif typeStr == "delete":
                rmLen = len(s.split("_")[-1]) + 1
                sNew = s[:-rmLen]
                cmds.rename(s, sNew)


    def rename(self):
        findStr = str(self.renameFindText.text())
        replaceStr = str(self.renameReplaceText.text())
        sList = cmds.ls(selection = True)
        for s in sList:
            sNew = s.replace(findStr, replaceStr)
            cmds.rename(s, sNew)


    def numberate(self):
        print todo


def main():
    nh = NameHelper()
    nh.show()

