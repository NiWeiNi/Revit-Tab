# -*- coding: utf-8 -*-
"""Number doors according to room number and assign department.
"""
__author__ = "nWn"
__title__ = "Number\n Doors"

# Import 
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms
import copy

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Function to check if element is in group
def insideGroup(element, groups):
	for g in groups:
		for id in g.GetMemberIds():
			if id == element.Id:
				return True

# Function to ungroup current group and store groups name and elements
def ungroup(group):
	gEIds = group.GetMemberIds()
	group.UngroupMembers()
	return gEIds

# Funtion to swap groups
def swapGroup(group, groupType):
	group.GroupType = groupType

# Function to number doors
def numberDoors():
	# Set the condition to run the script: Doors must have Department parameter
	params = doc.ParameterBindings.ForwardIterator()
	while params.MoveNext():
		for cat in params.Current.Categories:
			if cat.Name == "Doors" and params.Key.Name == "Department":

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
					# Case room is null leave Mark as it is and delete department
					else:
						doorNumbers.append(d.LookupParameter("Mark").AsString())
						department.append("")
						roomName.append("")
						roomNumber.append("")

				# Create a individual transaction to change the parameters
				t = DB.Transaction(doc, "Set Mark on Doors")
				# Start individual transaction
				t.Start()

				# Set Mark and Department in doors
				for d, n, dep, numb, nam in zip(doorsCollector, doorNumbers, department, roomNumber, roomName):
					# Use overloads with a string as IronPython will throw an error by using same string
					d.LookupParameter("Mark").Set.Overloads[str](n)
					d.LookupParameter("Department").Set.Overloads[str](dep)
					d.LookupParameter("Room Number").Set.Overloads[str](numb)
					d.LookupParameter("Room Name").Set.Overloads[str](nam)

				# Commit transaction
				t.Commit()
				
				# End function
				return True

	# Finish script if there is no required project parameter 
	forms.alert("Please create a Project Parameter for Doors called Department", ok = True, exitscript= True)

# Collect all groups
groupsCollector = DB.FilteredElementCollector(doc).OfClass(DB.Group)

# Collect all group types
gTypesCollector = DB.FilteredElementCollector(doc).OfClass(DB.GroupType)

# Select all doors
doorsFilter = DB.ElementCategoryFilter(DB.BuiltInCategory.OST_Doors)
doorsCollector = DB.FilteredElementCollector(doc).WherePasses(doorsFilter).WhereElementIsNotElementType()

# Variables to store critical data
gTypeIds = [x.GroupType.Id for x in groupsCollector]
gElemIds = [x.GetMemberIds() for x in groupsCollector]

# Ungroups the groups
# Create a individual transaction to change the parameters
t = DB.Transaction(doc, "Ungroup Groups")
# Start individual transaction
t.Start()
for g in groupsCollector:
	g.UngroupMembers()
# Commit transaction
t.Commit()

# Call function to number doors
numberDoors()