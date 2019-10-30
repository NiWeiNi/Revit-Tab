# -*- coding: utf-8 -*-
"""List all currently selected elements.
"""
__title__ = 'List\nSelection'
__author__ = "nWn"

# Import 
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Retrieve selected elements Ids
selection = uidoc.Selection
selectionIds = selection.GetElementIds()

# Check if Selection is empty
count = selectionIds.Count 
if count == 0:
	print "No element selected"
# Print selected elements
else:
	for id in selectionIds:
		try:
			e = doc.GetElement(id)
			print e.Name
		except:
			print ""