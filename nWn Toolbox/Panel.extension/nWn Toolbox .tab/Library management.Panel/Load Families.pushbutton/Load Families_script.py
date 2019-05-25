# -*- coding: utf-8 -*-
"""Load families from a directory.

Note:
Please be as specific as possible selecting the folder,
as this script that loads all families in subfolders."""
__title__ = 'Batch Load\nFamilies'
__author__ = "nWn"

# Import commom language runtime
import clr

# from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import Transaction, TransactionGroup, IFamilyLoadOptions

# Import Python modules
import os
import re

# Import libraries to create a Windows form
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Windows.Forms import FolderBrowserDialog
from System.Windows.Forms import DialogResult

# Store user specified path
directory = ""

# Create folder browser window 
dialog = FolderBrowserDialog()

# Record for user action and store selected path
if (dialog.ShowDialog() == DialogResult.OK):
	directory = dialog.SelectedPath

# Retrieve all pathfiles and names from directory and subdirectories
def retrieveFamilies(directory):
	familiesNames = list()
	for folderName, subFolders, files in os.walk(directory):
		# Check if there are Revit families
		families = re.compile(r"[^{ddd+}]\.rfa$")
		for file in files:
			# Assign matched files to a variable
			matched = families.search(file)
			if matched:
				# Get path of families
				filePath = os.path.join(folderName, file)
				familiesNames.append(filePath)
	return familiesNames

# Call function to search for families in path and subfolders
familiesList = retrieveFamilies(directory)

# Store current document into variable
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Class to define loading options, in 
class familyLoadOptions(IFamilyLoadOptions):
	def __init__(self, overwrite):
		self.bool = overwrite
	def OnFamilyFound(self, bool1, bool2):
		return self.bool
	def OnSharedFamilyFound(self, sfamily, bool1, familySource, bool2):
		return self.bool

# Create a individual transaction to change the parameters on sheet
t = Transaction(doc, "Batch Load Families")
# Start individual transaction
t.Start()

# Loop through families and load them into the project
loadedFam = list()
notLoadedFam = list()

for family in familiesList:
	try:
		doc.LoadFamily(family, familyLoadOptions(True))
		loadedFam.append(family)
	except:
		notLoadedFam.append(family)

# Commit individual transaction
t.Commit()

# Print message to user about results
if len(loadedFam) == 0:
	print("No family has been loaded")
else:
	print("The following families have been loaded: \n")
	print("\n".join(loadedFam))
if len(notLoadedFam) != 0:
	print("The following families load have failed: \n")
	print("\n".join(notLoadedFam))