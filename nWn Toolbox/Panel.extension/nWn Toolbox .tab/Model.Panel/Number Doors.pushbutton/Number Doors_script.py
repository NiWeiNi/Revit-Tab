# -*- coding: utf-8 -*-
"""Number doors according to room number.
"""
__author__ = "nWn"
__title__ = "Number\n Doors"

# Import 
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

# Set the condition to run the script: Doors must have Department parameter
#TODO

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Select all doors
doorsFilter = DB.ElementCategoryFilter(DB.BuiltInCategory.OST_Doors)
doorsCollector = DB.FilteredElementCollector(doc).WherePasses(doorsFilter).WhereElementIsNotElementType()

# Select all phases
phases = doc.Phases
phasesName = [ph.Name for ph in phases]

# Form to select phase
phaseForm = forms.SelectFromList.show(phasesName, title = "Select Phase")

# Retrieve selected phase
for ph in phases:
	if ph.Name == phaseForm:
		selectedPhase = ph

# Check doors ToRoom
toRooms = []
for d in doorsCollector:
	room = d.ToRoom[selectedPhase]
	toRooms.append(room)

# Set auxiliar variables
roomNumbers = [x.Number if x != None else "" for x in toRooms]
countNumbers = {}
finalList = []
department = []

# Loop through all  rooms
for r, d in zip(toRooms, doorsCollector):
	# Check room is not null
	if r != None:
		department.append(r.LookupParameter("Department").AsString())
		# Check room is not duplicated
		if r.Number not in countNumbers.keys():
			finalList.append(r.Number)
			countNumbers[r.Number] = 1
		# If room is duplicated, count the number
		else:
			countNumbers[r.Number] = countNumbers[r.Number] + 1
			if countNumbers[r.Number] == 2:
				finalList[finalList.index(r.Number)] = r.Number + "A"
				finalList.append(r.Number + "B")
			else:
				finalList.append(r.Number + chr(ord('@')+countNumbers[r.Number]))
	else:
		finalList.append(d.LookupParameter("Mark").AsString())
		department.append("")

# Create a individual transaction to change the parameters
t = DB.Transaction(doc, "Set Mark on Doors")
# Start individual transaction
t.Start()

# Set numbers to doors
for d, n, dep in zip(doorsCollector, finalList, department):
	d.LookupParameter("Mark").Set(n)
	d.LookupParameter("Department").Set(dep)

# Commit transaction
t.Commit()