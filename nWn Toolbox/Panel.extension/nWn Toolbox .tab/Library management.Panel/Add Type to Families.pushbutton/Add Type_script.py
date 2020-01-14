# -*- coding: utf-8 -*-
"""Add type to families or modify parameters in this type if it already exists"""
__title__ = 'Add Types\nto Families'
__author__ = "nWn"

# Import 
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Import Python modules
import os
import re

# Record for user action and store selected path
directory = forms.pick_folder()

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
