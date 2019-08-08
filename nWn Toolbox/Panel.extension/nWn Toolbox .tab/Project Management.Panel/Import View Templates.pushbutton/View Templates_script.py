# -*- coding: utf-8 -*-
"""Import View Templates.

NOTE: Only new View Templates are transferred. Same name VT won't be overriden
"""
__title__ = 'Import View\nTemplates'
__author__ = "nWn"

# Import commom language runtime
import clr

# Import C# List
from System.Collections.Generic import List, ICollection

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

# Retrieve all View Templates from the selected projects
viewsFilter = ElementCategoryFilter(BuiltInCategory.OST_Views)

viewTemplates = {}

for pro in selProject:
	viewsCollector = FilteredElementCollector(pro).WherePasses(viewsFilter)
	for view in viewsCollector:
		if view.IsTemplate == True:
			viewTemplates[view.Name + " - " + pro.Title] = view

# Display select view templates form
vTemplates = forms.SelectFromList.show(viewTemplates.keys(), "View Templates", 600, 300, multiselect=True)

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
			ElementTransformUtils.CopyElements(pro, vTId, doc, transIdent, copyPasteOpt)

# Commit transaction
t.Commit()