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
        self.numerateButton.pressed.connect(self.numerate)


    def suffix(self, typeStr):
        sList = cmds.ls(selection = True)
        suffixStr = "_" + str(self.suffixComboBox.currentText())
        for s in sList:
            if typeStr == "add":
                cmds.rename(s, s + suffixStr)
            elif typeStr == "delete":
                rmLen = len(s.split("_")[-1]) + 1
                sNew = s[:-rmLen]
                cmds.rename(s, sNew)


    def rename(self):
        sList = cmds.ls(selection = True)
        findStr = str(self.renameFindText.text())
        replaceStr = str(self.renameReplaceText.text())
        for s in sList:
            sNew = s.replace(findStr, replaceStr)
            cmds.rename(s, sNew)


    def numerate(self):
        try:
            sList = cmds.ls(selection = True)
            nText = str(self.numerateText.text())
            count = nText.count("#")
            newText = ""

            for n in range(len(sList)):
                # create a str with appropriate number of "#"
                findStr = "".ljust(count, "#")
                # see if str is in text, not separated
                if findStr in nText and count != 0:
                    # new string has appropriate number of "0"
                    replaceStr = str(n+1).zfill(count)
                    sNew = nText.replace(findStr, replaceStr)
                    cmds.rename(sList[n], sNew)
        except:
            cmds.error("ERROR: numerate text now working; check you text")


def main():
    nh = NameHelper()
    nh.show()

