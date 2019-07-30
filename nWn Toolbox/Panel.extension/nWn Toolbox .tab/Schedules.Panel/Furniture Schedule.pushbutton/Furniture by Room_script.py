# -*- coding: utf-8 -*-
"""Creates and fill parameters to allow schedule furniture by rooms.

NOTE: 
Creates a poject parameter if it is not already in the project."""
__title__ = 'Furniture\nby Room'
__author__ = "nWn"

# Import commom language runtime
import clr

# Import Revit DB
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, \
                            Transaction, TransactionGroup

# Import pyRevit forms
from pyrevit import forms

# Store current document to variable
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document

# Collects elements
furnitureCollector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Furniture) \
                                                .WhereElementIsNotElementType().ToElements()

# Collect phases
phases = doc.Phases

# create list of phases names
phaseNames = []
for phase in phases:
	phaseNames.append(phase.Name)

# Create form to select phase
phasesForm = forms.ask_for_one_item(phaseNames, default=phaseNames[-1], prompt=None, title='Select Phase')

# Retrieve phase object from user selection
for phase in phases:
	if phase.Name == phasesForm:
		phaseObject = phase

# Create a individual transaction
t = Transaction(doc, "Fill Furniture Room Parameter")
# Start individual transaction
t.Start()

# Retrieve room in where the furniture is located and set in furniture
param = "In Room"
message = ""
for f in furnitureCollector:
	try:
		roomNumber = f.Room[phaseObject].LookupParameter("Number").AsString()
	except:
		roomNumber = ""
	try:
		f.LookupParameter(param).Set(roomNumber)
	except:
		message = "Please add " + param + " parameter to project."

# Commit individual transaction
t.Commit()

# Print result
if len(message) > 0:
	print(message)
