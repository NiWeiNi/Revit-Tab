# -*- coding: utf-8 -*-
"""Import View Templates.

NOTE: Select View Templates to transfer.
"""
__title__ = 'Import View\nTemplates'
__author__ = "nWn"

# Import commom language runtime
import clr

# Import Revit DB
from Autodesk.Revit.DB import FilteredElementCollector, ElementTransformUtils, BuiltInCategory, \
                            ElementId, Transform, Transaction, TransactionGroup, ElementCategoryFilter

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

# Retrieve View Templates to transfer
fTemplatesIds = []
for vT in vTemplates:
	fTemplatesIds.append(viewTemplates[vT].Id)

print fTemplatesIds
# Transform object
transIdent = Transform.Identity

# ElementTransformUtils.CopyElements(destinationdoc, fTemplatesIds, doc, transIdent,  )

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