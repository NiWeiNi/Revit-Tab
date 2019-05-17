# -*- coding: utf-8 -*-
"""Load families from a directory.

Note:
Families in the project will be overridden."""
__author__ = "nWn"

# Import commom language runtime
import clr

# from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import Transaction, TransactionGroup

# Import Python modules
import os
import re

# Retrieve all pathfiles and names from directory and subdirectories
def retrieveFamilies(directory):
	familiesNames = list()
	for folderName, subFolders, files in os.walk(directory):
		# Check if there are Revit families
		families = re.compile(r".*\.rfa$")
		for file in files:
			# Assign matched files to a variable
			matched = families.search(file)
			# Get path of families
			filePath = os.path.join(folderName, file)
			familiesNames.append(filePath)
	return familiesNames

directory = r"C:\ProgramData\Autodesk\RVT 2018\Libraries\Australia\Doors"
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

print("The following families have been loaded:")
print("\n".join(familiesList))