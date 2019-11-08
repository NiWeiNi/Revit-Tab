# -*- coding: utf-8 -*-
"""Number doors according to room number and assign department.

NOTE: Room name will be assigned according to To Room parameter except rooms named Ensuites or Bathrooms that pick From Room.
"""
__author__ = "nWn"
__title__ = "Number\n Doors"

# Import 
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Function to check existance of project parameter
def checkProjParam(catName, paramName):
	# Set the condition to run the script: Doors must have Department parameter
	params = doc.ParameterBindings.ForwardIterator()
	while params.MoveNext():
		for cat in params.Current.Categories:
			if cat.Name == catName and params.Key.Name == paramName:
				return True
	# Finish script if there is no required project parameter 
	forms.alert("Please create Project Parameter named " + paramName + " under " + catName + " category.", ok = True, exitscript= True)

# Function to select phase
def selectPhase():
	# Select all phases
	phases = doc.Phases
	phasesName = [ph.Name for ph in phases]

	# Form to select phase
	phaseForm = forms.SelectFromList.show(phasesName, title = "Select Phase")
	return phaseForm

# Function to number doors
def numberDoors():

	# Check project parameters
	checkProjParam("Doors", "Department")
	checkProjParam("Doors", "Room Number")
	checkProjParam("Doors", "Room Name")
	checkProjParam("Doors", "Door Number")

	# Retrieve selected phase
	for ph in phases:
		if ph.Name == phaseForm:
			selectedPhase = ph

	# Check doors ToRoom
	rooms = []
	for d in doorsCollector:
		# Pick preferred ToRoom parameter as default room
		if d.ToRoom[selectedPhase] != None:
			room = d.ToRoom[selectedPhase]
		# Default to FromRoom
		else:
			room = d.FromRoom[selectedPhase]
		rooms.append(room)

	# Set auxiliar variables
	countNumbers = {}
	doorNumbers = []
	department = []
	roomName = []
	roomNumber = []

	# Loop through all  rooms
	for r, d in zip(rooms, doorsCollector):
		# Check room is not null
		if r != None:
			department.append(r.LookupParameter("Department").AsString())
			roomName.append(r.LookupParameter("Name").AsString())
			roomNumber.append(r.LookupParameter("Number").AsString())
			# Check room is not duplicated
			if r.Number not in countNumbers.keys():
				doorNumbers.append(r.Number)
				countNumbers[r.Number] = 1
			# If room is duplicated, count the number
			else:
				countNumbers[r.Number] = countNumbers[r.Number] + 1
				# Check if there is more than one instance of door in the room and name them accordngly
				if countNumbers[r.Number] == 2:
					doorNumbers[doorNumbers.index(r.Number)] = r.Number + "A"
					doorNumbers.append(r.Number + "B")
				else:
					doorNumbers.append(r.Number + chr(ord('@') + countNumbers[r.Number]))
		# Case room is null leave Door Number as it is and delete department
		else:
			doorNumbers.append(d.LookupParameter("Door Number").AsString())
			department.append("")
			roomName.append("")
			roomNumber.append("")

	# Create a individual transaction to change the parameters
	t = DB.Transaction(doc, "Set Door Number on Doors")
	# Start individual transaction
	t.Start()

	# Set Door Number and Department in doors
	# Door Number is set as instance parameter which value can vary across groups. Default Mark doesn't work properly as it needs to be ungrouped.
	for d, n, dep, numb, nam in zip(doorsCollector, doorNumbers, department, roomNumber, roomName):
		# Use overloads with a string as IronPython will throw an error by using same string
		d.LookupParameter("Door Number").Set.Overloads[str](n)
		d.LookupParameter("Department").Set.Overloads[str](dep)
		d.LookupParameter("Room Number").Set.Overloads[str](numb)
		d.LookupParameter("Room Name").Set.Overloads[str](nam)

	# Commit transaction
	t.Commit()


# Select all doors
doorsFilter = DB.ElementCategoryFilter(DB.BuiltInCategory.OST_Doors)
doorsCollector = DB.FilteredElementCollector(doc).WherePasses(doorsFilter).WhereElementIsNotElementType()

# Call function to number doors
numberDoors()