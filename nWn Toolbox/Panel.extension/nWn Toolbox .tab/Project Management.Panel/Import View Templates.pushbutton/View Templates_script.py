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
def retrieveVT(docList, currentDoc):
	storeDict = {}
	if isinstance(docList, list):
		for pro in docList:
			viewsCollector = FilteredElementCollector(pro).WherePasses(viewsFilter)
			for view in viewsCollector:
				if view.IsTemplate == True:
					storeDict[view.Name + " - " + pro.Title] = view
	elif currentDoc == True:
		viewsCollector = FilteredElementCollector(docList).WherePasses(viewsFilter)
		for view in viewsCollector:
			if view.IsTemplate == True:
				storeDict[view.Name] = view
	else:
		viewsCollector = FilteredElementCollector(docList).WherePasses(viewsFilter)
		for view in viewsCollector:
			if view.IsTemplate == True:
				storeDict[view.Name + " - " + docList.Title] = view
	return storeDict

# Retrieve all view templates from selected docs
viewTemplates = retrieveVT(selProject, False)

# Display select view templates form
vTemplates = forms.SelectFromList.show(viewTemplates.keys(), "View Templates", 600, 300, multiselect=True)

# Collect all View Templates in the current document
docTemplates = retrieveVT(doc, True)

# Remove view templates with same name
vTemplatesNoProj = []
for vT in vTemplates:
	for p in selProject:
		if p.Title in vT:
			vTemplatesNoProj.append(vT.replace(p.Title, ""))

# Remove duplicated view templates from selection
newVTemplates = []
uniqueTemplates = []
for vNoProj, vT in zip(vTemplatesNoProj, vTemplates):
	if vNoProj not in uniqueTemplates:
		uniqueTemplates.append(vNoProj)
		newVTemplates.append(vT)

vTemplates = newVTemplates

# Collect all views from the current document
docViewsCollector = FilteredElementCollector(doc).WherePasses(viewsFilter)

# Check for duplicate View Templates in the current project
dupViewTemplates = []
for vN, vT in docTemplates.items():
	for v in vTemplates:
		if vN in v:
			dupViewTemplates.append(vT)

# Views with view templates
def checkViewT(viewsList):
	viewsWVT = {}
	for v in viewsList:
		if v.ViewTemplateId != ElementId.InvalidElementId:
			viewsWVT.setdefault(v.ViewTemplateId.ToString(), []).append(v)
	return viewsWVT

# Transform object
transIdent = Transform.Identity
copyPasteOpt = CopyPasteOptions()

# Create single transaction and start it
t = Transaction(doc, "Copy View Templates")
t.Start()

# Check for all views that has a view template
vTIds = []
viewsWVT = checkViewT(docViewsCollector)
viewsFail = []
viewsSuccess = []
for vT in vTemplates:
	vTId = List[ElementId]()
	for pro in selProject:
		if pro.Title in vT:
			vTId.Add(viewTemplates[vT].Id)
			# Check if view template is used in current doc
			if vT.replace(" - " + pro.Title, "") not in docTemplates.keys():
				# Copy the selected View Template to current project
				ElementTransformUtils.CopyElements(pro, vTId, doc, transIdent, copyPasteOpt)
				continue
			else:
				vToApplyVT = []
				for k in viewsWVT.keys():
					views = viewsWVT[k]
					flag = True
					for v in views:
						if flag:
							elName = doc.GetElement(v.ViewTemplateId).Name
							if elName in vT:
								doc.Delete(v.ViewTemplateId)
								et = ElementTransformUtils.CopyElements(pro, vTId, doc, transIdent, copyPasteOpt)
							else:
								break
						try:
							v.ViewTemplateId = et[0]
							viewsSuccess.append(v.Name)
							flag = False
						except:
							viewsFail.append(v.Name)

# Commit transaction
t.Commit()

# Function to display result to user
def printMessage(resultList, failedList, message, messageWarning):
	if len(resultList) != 0:
		print(message)
		print("\n".join(resultList))
	if len(failedList) != 0:
		print(messageWarning)
		print("\n".join(resultList))

# Print message
printMessage(viewsSuccess, viewsFail, "The following view's view template have been changed:",
			"View templates failed to apply to views, make sure the proper view template type is named:")
