# -*- coding: utf-8 -*-
"""Create interior elevations for selected rooms and place them on sheets.

NOTE: 
"""
__author__ = "nWn"
__title__ = "Interior\n Elevations"

# Import 
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Rooms wrapper
class RoomsForm(forms.TemplateListItem):
	@ property
	def name(self):
		return '{} --- {}'.format(self.item.Number, self.item.LookupParameter("Name").AsString())

# View Type wrapper
class ElevForm(forms.TemplateListItem):
	@ property
	def name(self):
		return self.item.LookupParameter("Type Name").AsString()

# Title Block wrapper
class TitleBlockForm(forms.TemplateListItem):
	@ property
	def name(self):
		return '{} --- {}'.format(self.item.LookupParameter("Family Name").AsString(), self.item.LookupParameter("Type Name").AsString())

# Function alert and quit
def alert(message):
	return forms.alert(message, ok = True, exitscript= True)

# Function to display select room
def roomElev():
	# Collect all rooms
	rooms = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Rooms)
	# Create set of rooms
	roomNumber = sorted([RoomsForm(x) for x in rooms], key=lambda x: x.Number)
	# Prompt selection list
	return forms.SelectFromList.show(roomNumber, "Rooms to Elevate", 600, 600, multiselect = True)

# Retrieve ViewFamilyType Id
def viewTypeId():
	# Collect all viewType
	elevCollector = DB.FilteredElementCollector(doc).OfClass(DB.ViewFamilyType)
	elevs = [x for x in elevCollector if x.LookupParameter("Family Name").AsString() == "Elevation"]
	# Check if user's input is required
	if len(elevs) > 1:
		elevNames = sorted([ElevForm(x) for x in elevs], key=lambda x: x.FamilyName)
		# Prompt selection list
		return forms.SelectFromList.show(elevNames, "Elevation Type", 600, 300).Id
	elif len(elevs) == 1:
		return elevs[0].Id
	else:
		alert("No Elevation Marker has been defined in the project. Please create an Elevation Marker.")
	
# Retrieve Title Block Type Id
def titleTypeId():
	# Collect all title block types
	titleBlocksCollector = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_TitleBlocks).WhereElementIsElementType()
	# Check if user's input is required
	titleBlocks = list(titleBlocksCollector)
	if len(titleBlocks) > 1:
		# Prompt selection list
		titleNames = sorted([TitleBlockForm(x) for x in titleBlocksCollector], key=lambda x: x.FamilyName)
		return forms.SelectFromList.show(titleNames, "Title Block Type", 600, 300).Id
	elif len(titleBlocks) == 1:
		return titleBlocks[0].Id
	else:
		alert("No Title Block loaded. Please load a Title Block.")

# Retrieve boundaries of rooms
def boundaries(room):
	# Spatial element boundary options class
	sEBO = DB.SpatialElementBoundaryOptions()
	# Retrieve boundaries
	bounda = room.GetBoundarySegments(sEBO)
	return bounda

# Function to retrieve center of room
def roomCenter(room):
	per = room.Perimeter
	return per

# Function to create sheet
def createSheet(room, titleBlockId, prefix = "INTERIOR ELEVATIONS"):
	sheet = DB.ViewSheet.Create(doc, titleBlockId)
	sheet.Name = room.Number + " - " + prefix

# Function to create elevations
def createElev(rooms, viewTypeId):
	for r in rooms:
		if r.Location != None:
			marker = DB.ElevationMarker.CreateElevationMarker(doc, viewTypeId, r.Location.Point, 5)
			for intView in range(0,4):
				marker.CreateElevation(doc, doc.ActiveView.Id, intView)

# Prompt to select rooms
roomsElev = roomElev()
viewTypeId = viewTypeId()
titleBlockId = titleTypeId()

# Create transaction and start it
t = DB.Transaction(doc, "Create Markers")
t.Start()
# Create elevation markers
createElev(roomsElev, viewTypeId)
# Commit transaction
t.Commit()