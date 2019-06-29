# -*- coding: utf-8 -*-
"""Isolates selected categories and overriden the rest of them with 90% transparency.
"""
__title__ = 'Isolate\nCategory'
__author__ = "nWn"

# Import commom language runtime
import clr

# Import Revit UI
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.UI import TaskDialog

# Import Revit DB
from Autodesk.Revit.DB import OverrideGraphicSettings, Transaction

# Store current document to variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Retrieve current view
activeView = doc.ActiveView

# Retrieve all categories in the document
docCat = doc.Settings.Categories

# Show task dialog to inform user
TaskDialog.Show("Select elements", "Select elements from categories to isolate")

# Select elements
objType = ObjectType.Element
selection = uidoc.Selection.PickObjects(objType, "Pick elements to isolate with transparency")

# Store categories of the selected elements
categories = []
for e in selection:
	elem = doc.GetElement(e.ElementId)
	cat = doc.GetElement(e.ElementId).Category.Name
	# Check if element is group or assembly to extract elements
	if cat == "Assemblies" or cat == "Model Groups":
		ids = elem.GetMemberIds()
		# Get elements category inside groups or assemblies
		for id in ids:
			catsub = doc.GetElement(id).Category.Name
			categories.append(catsub)
	else:
		categories.append(cat)

# Override tranparency settings
overtransparency = OverrideGraphicSettings()
overtransparency.SetSurfaceTransparency(50)

# Create a individual transaction
t = Transaction(doc, "Override category visibility")
# Start individual transaction
t.Start()

# Override all categories transparency
for c in docCat:
	if c.Name not in categories:
		try:
			activeView.SetCategoryOverrides(c.Id, overtransparency)
		except:
			pass

# Commit transaction
t.Commit()