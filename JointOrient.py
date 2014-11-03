TITLE = "Joint Orientation"
DESCRIPTION = "Creates two locations for up and x aim direction; orientates joints accordingly."
IMAGE = "commandButton.png"
RUN_COMMAND = "import JointOrient as jo; reload(jo); jo.main();"
ICON_LABEL = "JOr"

import os
import maya.cmds as cmds
import PySideUtil as psUtil
reload(psUtil)
from functools import partial

thisdirectory = os.path.dirname(os.path.realpath(__file__))
uiFile = os.path.join(thisdirectory, "ui", "JointOrient.ui")
form_class, base_class = psUtil.loadUiType(uiFile)


class JointOrient(base_class, form_class):
    def __init__(self, parent = psUtil.getMayaWindow()):
        super(JointOrient, self).__init__(parent)
        self.setupUi(self)
        self.connectUi()
        self.locatorUpStr = "_up_locator";
        self.locatorAimStr = "_aim_locator";
        self.jointDict = {}


    def connectUi(self):
        self.createButton.pressed.connect(self.createLocators)
        self.deleteButton.pressed.connect(self.deleteLocators)
        self.orientButton.pressed.connect(self.orientJoints)
        # display local axis
        self.axisOnButton.pressed.connect(partial(self.toggleDisplayLocalAxis, "on"))
        self.axisOffButton.pressed.connect(partial(self.toggleDisplayLocalAxis, "off"))


    def toggleDisplayLocalAxis(self, value = "on"):
        valueDict = {"off" : 0, "on": 1}
        jointList = cmds.ls(type = 'joint', selection = True)
        for joint in jointList:
            cmds.setAttr(joint + ".displayLocalAxis", valueDict[value])


    def orientJoints(self):
        # check which aim axis to rotate
        for i in range(self.aimGridLayout.count()):
            item = (self.aimGridLayout.itemAt(i)).widget()
            if item.isChecked():
                aimAxis = (item.text()).__str__()
        # check which up axis to rotate
        for i in range(self.upGridLayout.count()):
            item = (self.upGridLayout.itemAt(i)).widget()
            if item.isChecked():
                upAxis = (item.text()).__str__()

        # rotate joints for selected joints in dictionary
        jointList = cmds.ls(type = 'joint', selection = True)
        for joint in jointList:
            if joint in self.jointDict.keys():
                self.zeroJointOrient(joint)
                locatorAim = self.jointDict[joint]["aim"]
                locatorUp = self.jointDict[joint]["up"]

                # needed values
                vectorDict = {"x" : [1.0, 0.0, 0.0], "y" : [0.0, 1.0, 0.0], "z" : [0.0, 0.0, 1.0],
                                "-x" : [-1.0, 0.0, 0.0], "-y" : [0.0, -1.0, 0.0], "-z" : [0.0, 0.0, -1.0]}
                jointPos = cmds.xform(joint, query = True, worldSpace = True, translation = True)

                # get locator aim values
                if locatorUp is not None:
                    locatorUpPos = cmds.xform(locatorUp, query = True, worldSpace = True, translation = True)
                    upVector = vectorDict[upAxis]
                
                if locatorAim is not None:
                    locatorAimPos = cmds.xform(locatorAim, query = True, worldSpace = True, translation = True)
                    aimVector = vectorDict[aimAxis]

                # aim and up constrain
                if locatorUp is not None and locatorAim is not None:
                    constraint = cmds.aimConstraint(locatorAim, joint, aimVector = aimVector, upVector = upVector, 
                        worldUpType = "object", worldUpObject = locatorUp)[0]
                # aim constrain
                elif locatorUp is None and locatorAim is not None:
                    constraint = cmds.aimConstraint(locatorAim, joint, aimVector = aimVector)[0]
                # up constraint
                elif locatorUp is not None and locatorAim is None:
                    constraint = cmds.aimConstraint(locatorUp, joint, aimVector = upVector)[0]

                # clean joint
                cmds.delete(constraint)
                self.cleanJointRotation(joint)


    def zeroJointOrient(self, joint):
        tempList = ["X", "Y", "Z"]
        for xyz in tempList:
            cmds.setAttr(joint + ".jointOrient" + xyz, 0)


    def cleanJointRotation(self, joint):
        '''copy the values from rotation to orientation, and make the rotate values to 0,0,0'''
        tempList = ["X", "Y", "Z"]
        for xyz in tempList:
            value = cmds.getAttr(joint + ".rotate" + xyz)
            cmds.setAttr(joint + ".jointOrient" + xyz, value)
            cmds.setAttr(joint + ".rotate" + xyz, 0)


    def createLocators(self):
        # check if aim/up locator is checked
        createUp = None
        createAim = None
        if self.upCheckBox.isChecked():
            createUp = True
        if self.aimCheckBox.isChecked():
            createAim = True

        # start creating locators
        jointList = cmds.ls(type = 'joint', selection = True)
        for joint in jointList:
            # remove unicode 'u'
            joint = joint.encode('ascii', 'ignore')
            self.jointDict[joint] = {}

            # find location of each joint selected
            location = cmds.xform(joint, query = True, worldSpace = True, translation = True)
            rotate = cmds.xform(joint, query = True, worldSpace = True, rotation = True)

            # create locators if checked and they don't already exist
            # up
            if cmds.objExists(joint + self.locatorUpStr):
                self.jointDict[joint]["up"] = joint + self.locatorUpStr
            elif createUp is not None:
                upLocator = (cmds.spaceLocator(name = joint + self.locatorUpStr, position = location)[0]).encode('ascii', 'ignore')
                cmds.move(location[0], location[1], location[2], upLocator+".scalePivot", upLocator+".rotatePivot", absolute=True)
                cmds.setAttr(upLocator + ".rotateX", rotate[0])
                cmds.setAttr(upLocator + ".rotateY", rotate[1])
                cmds.setAttr(upLocator + ".rotateZ", rotate[2])
                cmds.select(upLocator)
                self.jointDict[joint]["up"] = upLocator
            else:
                self.jointDict[joint]["up"] = None
            # aim
            if cmds.objExists(joint + self.locatorAimStr):
                self.jointDict[joint]["aim"] = joint + self.locatorAimStr
            elif createAim is not None:
                aimLocator = (cmds.spaceLocator(name = joint + self.locatorAimStr, position = location)[0]).encode('ascii', 'ignore')
                cmds.move(location[0], location[1], location[2], aimLocator+".scalePivot", aimLocator+".rotatePivot", absolute=True)
                cmds.setAttr(aimLocator + ".rotateX", rotate[0])
                cmds.setAttr(aimLocator + ".rotateY", rotate[1])
                cmds.setAttr(aimLocator + ".rotateZ", rotate[2])
                cmds.select(aimLocator)
                self.jointDict[joint]["aim"] = aimLocator
            else:
                self.jointDict[joint]["aim"] = None


    def deleteLocators(self):
        for joint in self.jointDict:
            if self.jointDict[joint]["up"] is not None:
                cmds.delete(self.jointDict[joint]["up"])
            if self.jointDict[joint]["aim"] is not None:
                cmds.delete(self.jointDict[joint]["aim"])


def main():
    jo = JointOrient()
    jo.show()

