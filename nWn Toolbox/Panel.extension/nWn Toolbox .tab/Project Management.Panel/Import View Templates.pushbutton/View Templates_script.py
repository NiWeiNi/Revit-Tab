# -*- coding: utf-8 -*-
"""Import View Templates.

NOTE: Only new View Templates are transferred. Same name VT won't be overriden
"""
__title__ = 'Import View\nTemplates'
__author__ = "nWn"

# Import commom language runtime
import clr

# Import C# List
from System.Collections.Generic import List

# Import Revit DB
from Autodesk.Revit.DB import FilteredElementCollector, ElementTransformUtils, BuiltInCategory, \
                            ElementId, Transform, CopyPasteOptions, Transaction, TransactionGroup, ElementCategoryFilter

# Import pyRevit forms
from pyrevit import forms

# Store current document to variable
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Select opened documents to transfer View Templates
selProject = forms.select_open_docs(title="Select project/s to transfer View Templates", button_name='OK', width=500, multiple=True, filterfunc=None)

# Filter Views
viewsFilter = ElementCategoryFilter(BuiltInCategory.OST_Views)

# Function to retrieve View Templates
def retrieveVT(docList):
	storeDict = {}
	if isinstance(docList, list):
		for pro in docList:
			viewsCollector = FilteredElementCollector(pro).WherePasses(viewsFilter)
			for view in viewsCollector:
				if view.IsTemplate == True:
					storeDict[view.Name + " - " + pro.Title] = view
	else:
		viewsCollector = FilteredElementCollector(docList).WherePasses(viewsFilter)
		for view in viewsCollector:
			if view.IsTemplate == True:
				storeDict[view.Name + " - " + docList.Title] = view
	return storeDict

# Retrieve all view templates from selected docs
viewTemplates = retrieveVT(selProject)

# Display select view templates form
vTemplates = forms.SelectFromList.show(viewTemplates.keys(), "View Templates", 600, 300, multiselect=True)

# Collect all View Templates in the current document
docTemplates = retrieveVT(doc)

# Collect all views from the current document
docViewsCollector = FilteredElementCollector(doc).WherePasses(viewsFilter)

# Check for all views that has a view template
for v in docViewsCollector:
	if v.ViewTemplateId != ElementId.InvalidElementId:
		print v.ViewTemplateId

# Check for duplicate View Templates in the current project
# TODO

# Transform object
transIdent = Transform.Identity
copyPasteOpt = CopyPasteOptions()

# Create single transaction and start it
t = Transaction(doc, "Copy View Templates")
t.Start()

# Retrieve View Templates to transfer
for vT in vTemplates:
	vTId = List[ElementId]()
	for pro in selProject:
		if pro.Title in vT:
			vTId.Add(viewTemplates[vT].Id)
			# Copy the selected View Template to current project
			et = ElementTransformUtils.CopyElements(pro, vTId, doc, transIdent, copyPasteOpt)

# Commit transaction
t.Commit()

# Function to display result to user
def printMessage(resultList, message):
	if len(resultList) != 0:
		print(message)
		print("\n".join(resultList))

# Print message
printMessage([], "The following View Templates were transferred:")
printMessage([], "Non transferred View Templates:")