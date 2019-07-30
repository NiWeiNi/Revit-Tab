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

# Retrieve room in where the furniture is located
for f in furnitureCollector:
	f.Room[phaseObject]

"""
# Create a Transaction group to group all subsequent transactions
tg = TransactionGroup(doc, "Update Drawn By and Checked By")

# Start the group transaction
tg.Start()

# Create a individual transaction to change the parameters on sheet
t = Transaction(doc, "Change Sheets Name")

# Start individual transaction
t.Start()

# Variable to store modified sheets
modSheets = list()

# Define function to modify parameter
def modParameter(param, checkEmpty, inputParam):
    # Store the sheet number parameter in variable
    sheetNumber = sheet.LookupParameter("Sheet Number").AsString()
    # Retrieve sheet parameter
    sheetDrawn = sheet.LookupParameter(param)
    # Check if it is by default and input is not empty, set it with user input
    if sheetDrawn.AsString() == checkEmpty and inputParam != "":
        sheetDrawn.Set(inputParam)
        # Check if the sheet has been previously modified and append to list
        if sheetNumber not in modSheets:
            modSheets.append(sheetNumber)

# Loop through all sheets
for sheet in sheetsCollector:
    # Run function to modify Drawer
    modParameter("Drawn By", "Author", nameDrawer)
    # Call function to modify Checker
    modParameter("Checked By", "Checker", nameChecker)

# Commit individual transaction
t.Commit()

# Combine all individual transaction in the group transaction
tg.Assimilate()

# Print all changed sheets
print("The following sheets have been modified: \n\n" + "\n".join(modSheets))

"""