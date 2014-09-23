'''
Note: pyinstaller
pyinstaller --onefile "pythonfile"
'''

import os
import shutil
import filecmp

class SetupScripts:
	
	def __init__(self):
		self.filesInPackage = os.listdir()
		self.shelfName = "shelf_Emily_Scripts"
		self.message = ""


	def setup(self):
		# set global mayaScriptPath if it's found
		# if not, do not do anything
		self.updateMayaScriptPath()
		# update shelf and script
		self.updateEmilyMaya(self.getEmilyScriptList(), self.getMayaScriptPath())
		self.updateEmilyMaya([self.shelfName + ".mel"], self.getMayaShelvesPath())
		self.reloadShelfFile()
		self.printMessage(self.message)
		print(os.name)


	def printMessage(self, text):
		print(text)


	def saveMessage(self, text):
		self.message += text + "\n" 


	def updateMayaScriptPath(self, inputPath = ""):
		if self.getMayaScriptPath() is not None and inputPath == "":
			self.mayaScriptPath = self.getMayaScriptPath()
		elif os.path.isdir(inputPath):
			self.mayaScriptPath = inputPath
		else:
			self.saveMessage("WARNING: cound not add scripts, please check path")


	def updateEmilyMaya(self, emilyList, path):
		'''
		Add script to maya folder if missing;
		else, check to see if it is different
		and update if needed.
		'''
		mayaList = os.listdir(path)
		# make sure there are emily scripts
		if emilyList != []:
			self.saveMessage("Path: " + path)
			for eScript in emilyList:
				mayaVersion = path + "/" + eScript
				# if the script is already in maya, check if it's the same
				# if not, remove it and replace it with new version
				if eScript in path and not filecmp.cmp(eScript, mayaVersion):
					self.saveMessage("Removing and updating: " + eScript)
					os.remove(mayaVersion)
					shutil.copy(eScript, path)
				# if the script is not in maya, add it
				elif eScript not in mayaList:
					shutil.copy(eScript, path)
					self.saveMessage("Added: " + eScript)
				# nothing need to be updated or moved
				else:
					self.saveMessage("No files to move or update")
		else:
			self.saveMessage("No files to move")


	def getEmilyScriptList(self):
		scriptList = []
		# find all python scripts that are not this one
		for oneFile in self.filesInPackage:
			if oneFile.endswith(".py") and oneFile != __file__:
				scriptList.append(oneFile)
		return scriptList


	def getMayaPrefPath(self):
		name = os.getlogin()
		mayaPath = "/Users/" + name + "/Library/Preferences/Autodesk/maya/"
		year = 2011
		maxYear = 3000
		recentYear = 0
		done = False
		addPath = ""

		# make sure the maya path is correct
		if os.path.isdir(mayaPath):
			dirList = os.listdir(mayaPath)
			# start from 2011, check for the most recent version of maya
			while year < maxYear or done == False:
				for d in dirList:
					if str(year) in d and year > recentYear:
						recentYear = year
						addPath = d
						done = True
				year += 1

		# make sure the year/script path is correct
		mayaPath += addPath + "/prefs"
		if os.path.isdir(mayaPath):
			return mayaPath
		else:
			return None


	def getMayaScriptPath(self):
		try:
			path = self.getMayaPrefPath() + "/scripts"
			if os.path.isdir(path):
				return path
		except:
			return None


	def getMayaShelvesPath(self):
		try:
			path = self.getMayaPrefPath() + "/shelves"
			if os.path.isdir(path):
				return path
		except:
			return None


	def reloadShelfFile(self):
		'''
		Create shelf mel file for scripts in the package
		'''
		shelfFile = self.shelfName + ".mel"
		fp = open(shelfFile, 'w+')
		fp.write(self.getShelfHeaderText())
		# check if script is already in shelf file
		for script in self.getEmilyScriptList():
			sfp = open(script)
			text = self.getScriptShelfText(
					script,
					(sfp.readline()).split("\"")[1], \
					(sfp.readline()).split("\"")[1], \
					(sfp.readline()).split("\"")[1], \
					(sfp.readline()).split("\"")[1])
					# title, desc, image, code
			fp.write(text)
		fp.write("\n}")
		self.saveMessage("Updated: " + shelfFile)



	def getShelfHeaderText(self):
		return "global proc " + self.shelfName + " () { \
				\n\tglobal string $gBuffStr; \
				\n\tglobal string $gBuffStr0; \
    			\n\tglobal string $gBuffStr1;\n"


	def getScriptShelfText(self, script, title, desc, image, code):
		'''
		Return text for each script to be added
		'''
		if code == "":
			code = script
		text = "\n\n\tshelfButton"
		shelfItemAttrTextDict = ["enableCommandRepeat 1",
    							"enable 1", 
    							"width 35", 
    							"height 35", 
    							"manage 1",
    							"visible 1",
    							"preventOverride 0",
    							"annotation \"" + desc + "\"", 	# what it does
    							"enableBackground 0",
    							"align \"center\"",
    							"label \"" + title + "\"", 		# title
    							"labelOffset 0",
    							"font \"plainLabelFont\"",
    							"overlayLabelColor 0.8 0.8 0.8",
    							"overlayLabelBackColor 0 0 0 0.25",
    							"image \"" + image + "\"", 		# image link
    							"image1 \"" + image + "\"",		# image link
    							"style iconOnly",
    							"marginWidth 1",
    							"marginHeight 1",
    							"command \"" + code + "\"",		# code
    							"sourceType python",
    							"commandRepeatable 1",
    							"flat 1"]
		for label in shelfItemAttrTextDict:
			text += "\n\t\t-" + label
		return text + "\n\t;"



def main():
	ss = SetupScripts()
	ss.setup()


if __name__ == '__main__':
    main()