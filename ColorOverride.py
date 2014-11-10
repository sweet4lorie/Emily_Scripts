TITLE = "Color Override"
DESCRIPTION = "Helps with color override"
IMAGE = "commandButton.png"
RUN_COMMAND = "import ColorOverride as co; reload(co); co.main();"
ICON_LABEL = "Color"

import os
import maya.cmds as cmds
import PySideUtil as psUtil
reload(psUtil)
from functools import partial

thisdirectory = os.path.dirname(os.path.realpath(__file__))
uiFile = os.path.join(thisdirectory, "ui", "ColorOverride.ui")
form_class, base_class = psUtil.loadUiType(uiFile)


class ColorOverride(base_class, form_class):
    def __init__(self, parent = psUtil.getMayaWindow()):
        super(ColorOverride, self).__init__(parent)
        self.setupUi(self)
        
        self.colorList = self.getColorList()
        self.defaultColorList = [17, 13, 6, 3]
        self.connectUi()


    def connectUi(self):
        self.defaultColor0Button.pressed.connect(partial(self.setColor, self.defaultColorList[0]))
        self.defaultColor1Button.pressed.connect(partial(self.setColor, self.defaultColorList[1]))
        self.defaultColor2Button.pressed.connect(partial(self.setColor, self.defaultColorList[2]))
        self.defaultColor3Button.pressed.connect(partial(self.setColor, self.defaultColorList[3]))
        self.sliderHorizontalSlider.valueChanged.connect(self.slider)
        self.overrideButton.pressed.connect(partial(self.setColor))
        self.clearButton.pressed.connect(self.clear)


    def getSliderColor(self):
        print int(self.sliderHorizontalSlider.value() / 3.15)
        return int(self.sliderHorizontalSlider.value() / 3.15)


    def slider(self):
        index = self.getSliderColor()
        style = "background-color: rgb(" + self.colorList[index][0] + ", " + \
                                    self.colorList[index][1] + ", " + \
                                    self.colorList[index][2] + ")"
        self.sliderButton.setStyleSheet(style)


    def setColor(self, colorNum = -1):
        # get color from slider if one is not included
        if colorNum == -1:
            colorNum = self.getSliderColor()
        sList = cmds.ls(selection = True)
        for s in sList:
            cmds.setAttr(s + ".overrideEnabled", 1)
            cmds.setAttr(s + ".overrideColor", colorNum)


    def clear(self):
        sList = cmds.ls(selection = True)
        for s in sList:
            cmds.setAttr(s + ".overrideEnabled", 0)


    def getColorList(self):
        return [    ["120", "120", "120"],    # 0: gray/default
                    ["0", "0", "0"],          # 1: black
                    ["64", "64", "64"],       # 2: dark gray
                    ["128", "128", "128"],    # 3: light gray * 
                    ["155", "0", "40"],       # 4: crimson
                    ["0", "4", "96"],         # 5: dark blue
                    ["0", "0", "225"],        # 6: blue *
                    ["0", "70", "25"],        # 7: dark green
                    ["38", "0", "67"],        # 8: dark purple
                    ["200", "0", "200"],      # 9: magenta
                    ["138", "72", "51"],      # 10: sienna
                    ["63", "35", "31"],       # 11: dark brown
                    ["153", "38", "0"],       # 12: red sienna
                    ["255", "0", "0"],        # 13: red *
                    ["0", "0", "255"],        # 14: green
                    ["0", "65", "153"],       # 15: sea blue
                    ["255", "255", "255"],    # 16: white
                    ["255", "255", "0"],      # 17: yellow *
                    ["100", "220", "255"],    # 18: sky blue
                    ["67", "255", "163"],     # 19: light green
                    ["255", "176", "176"],    # 20: pink
                    ["228", "172", "121"],    # 21: light brown
                    ["225", "225", "99"],     # 22: light yellow
                    ["0", "153", "84"],       # 23: forest green
                    ["161", "105", "48"],     # 24: brown
                    ["159", "161", "48"],     # 25: yellow-green
                    ["104", "161", "48"],     # 26: dirty green
                    ["48", "161", "93"],      # 27: dark rich green
                    ["48", "161", "161"],     # 28: teal
                    ["48", "103", "161"],     # 29: light sea blue
                    ["111", "48", "161"],     # 30: purple
                    ["161", "48", "105"]      # 31: dark magenta
                ]

def main():
    co = ColorOverride()
    co.show()

