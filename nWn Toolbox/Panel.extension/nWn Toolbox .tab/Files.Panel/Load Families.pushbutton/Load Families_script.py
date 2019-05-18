# -*- coding: utf-8 -*-
"""Load families from a directory.

Note:
As this script will load all families in subfolders,
please be as specific as possible selecting the folder."""
__author__ = "nWn"

# Import commom language runtime
import clr

# from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import Transaction, TransactionGroup

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
		families = re.compile(r"\.rfa$")
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


# Create a individual transaction to change the parameters on sheet
t = Transaction(doc, "Batch Load Families")
# Start individual transaction
t.Start()

# Loop through families and load them into the project
loadedFam = list()
notLoadedFam = list()

for family in familiesList:
	try:
		doc.LoadFamily(family)
		loadedFam.append(family)
	except:
		notLoadedFam.append(fam)

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