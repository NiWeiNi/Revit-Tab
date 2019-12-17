# -*- coding: utf-8 -*-
"""Isolates selected categories and overriden the rest of them with 50% transparency.
"""
__title__ = 'Isolate\nCategory'
__author__ = "nWn"

# Import 
from pyrevit import revit, DB, UI
from pyrevit import script
from pyrevit import forms

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Function to retrieve all categories in the document
def cat():
	docCat = doc.Settings.Categories
	return docCat

# Function to pick elements
def pickEl():
	# Show task dialog to inform user
	UI.TaskDialog.Show("Select elements", "Select elements of categories to isolate")
	# Select elements
	objType = UI.Selection.ObjectType.Element
	selection = uidoc.Selection.PickObjects(objType, "Pick elements to isolate with transparency")
	return selection

# Function to retrieve categories from selection
def retCat(selection):
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
	return categories

# Function to override transparency
def overCat(categories, docCat):
	# Retrieve current view
	activeView = doc.ActiveView
	# Override tranparency settings
	overtransparency = DB.OverrideGraphicSettings()
	overtransparency.SetSurfaceTransparency(50)

	# Create a individual transaction
	t = DB.Transaction(doc, "Override category visibility")
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

# Function to override categories
def overrideCat():
	sel = pickEl()
	cats = retCat(sel)
	overCat(cats, cat())

overrideCat()