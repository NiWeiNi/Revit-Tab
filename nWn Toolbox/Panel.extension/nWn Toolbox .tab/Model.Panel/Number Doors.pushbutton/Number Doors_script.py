# -*- coding: utf-8 -*-
"""Number doors according filling Door Number, Room Number, Room Name, Department and Level Sorted.

NOTE: Room name will be assigned according to To Room parameter except for the selected rooms which will use From Room.
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
def selectPhase(doorsCollector):
	phase = ""
	for d in doorsCollector:
		phaseId = d.CreatedPhaseId
		phase = doc.GetElement(phaseId)
		break
	return phase

# Function to display select room names
def roomNames():
	# Collect all rooms
	rooms = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Rooms)
	# Create set of rooms
	roomNames = [r.LookupParameter("Name").AsString() for r in rooms]
	roomSet = sorted(set(roomNames))
	# Prompt selection list
	return forms.SelectFromList.show(roomSet, "Rooms with reverse opening", 600, 600, multiselect = True)

# Function to retrieve door rooms
def doorRooms(doorsCollector, selectedPhase, roomsExcluded):
	rooms = []
	room = None
	for d in doorsCollector:
		toRoom = d.ToRoom[selectedPhase]
		fromRoom = d.FromRoom[selectedPhase]
		# Pick preferred ToRoom parameter as default room
		if toRoom != None:
			if fromRoom != None and fromRoom.LookupParameter("Name").AsString() in roomsExcluded:
				room = fromRoom
			else:
				room = toRoom
		# Default to FromRoom
		else:
			room = fromRoom
		rooms.append(room)
	return rooms

# Function to fill in sorted levels
def sortLevels(doorsCollector):
	# Collect all levels
	levelsCollector = DB.FilteredElementCollector(doc).OfClass(DB.Level).ToElements()
	# Sort levels by elevation
	sortedL = sorted(levelsCollector, key=lambda x: x.LookupParameter("Elevation").AsDouble())
	# Create dictionary with level name and sorted level name
	levelCount = len(sortedL)
	prefix = range(levelCount)
	levelName = [l.Name for l in sortedL]
	sortedLevel = ["{:02} - {}".format(a, b) for a, b in zip(prefix, levelName)]
	levelNameSorted = dict(zip(levelName, sortedLevel))
	# Create sorted level name for all doors
	sortedDoorLevels = []
	for d in doorsCollector:
		try:
			eId = d.get_Parameter(DB.BuiltInParameter.FAMILY_LEVEL_PARAM).AsElementId()
			level = doc.GetElement(eId)
			if level.Name in levelName:
				sortedDoorLevels.append(levelNameSorted[level.Name])
		except:
			sortedDoorsLevels.append("")
	return sortedDoorLevels

# Function to number doors
def numberDoors(doorsCollector):
	# Check project parameters
	checkProjParam("Doors", "Department")
	checkProjParam("Doors", "Room Number")
	checkProjParam("Doors", "Room Name")
	checkProjParam("Doors", "Door Number")

	# Select phase
	selectedPhase = selectPhase(doorsCollector)

	# Select rooms with reverse door openings
	reverseRooms = roomNames()

	# Set auxiliar variables
	countNumbers = {}
	doorNumbers = []
	department = []
	rooms = doorRooms(doorsCollector, selectedPhase, reverseRooms)
	sortedLevels = sortLevels(doorsCollector)
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
	for d, n, dep, numb, nam, sL in zip(doorsCollector, doorNumbers, department, roomNumber, roomName, sortedLevels):
		# Use overloads with a string as IronPython will throw an error by using same string
		d.LookupParameter("Door Number").Set.Overloads[str](n)
		d.LookupParameter("Department").Set.Overloads[str](dep)
		d.LookupParameter("Room Number").Set.Overloads[str](numb)
		d.LookupParameter("Room Name").Set.Overloads[str](nam)
		d.LookupParameter("Level Sorted").Set.Overloads[str](sL)

	# Commit transaction
	t.Commit()

# Retrieve Door Schedule
views = DB.FilteredElementCollector(doc).OfClass(DB.View)
scheId = [x.Id for x in views if x.Name.lower() == "Door Schedule".lower()]

# Retrieve doors from schedule
doorsSchedule = DB.FilteredElementCollector(doc, scheId[0])
doorsCollector = [d for d in doorsSchedule if d.Category.Name == "Doors"]

# Call function to number doors
numberDoors(doorsCollector)