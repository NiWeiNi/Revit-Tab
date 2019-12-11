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

# View Template wrapper
class ViewTempForm(forms.TemplateListItem):
	@ property
	def name(self):
		return self.item.Name

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

# Retrieve view templates
def viewTempId():
	# Collect all views
	viewsCollector = DB.FilteredElementCollector(doc).OfClass(DB.View)
	# Filter view templates
	viewTemplates = [v for v in viewsCollector if v.IsTemplate]
	# Prompt selection list
	viewTemps = sorted([ViewTempForm(x) for x in viewTemplates], key=lambda x: x.Name)
	return forms.SelectFromList.show(viewTemps, "View Template", 600, 300).Id

# Retrieve boundaries of rooms
def boundaries(room):
	# Spatial element boundary options class
	sEBO = DB.SpatialElementBoundaryOptions()
	# Retrieve boundaries
	bounda = room.GetBoundarySegments(sEBO)
	return bounda

# Function to extract points from boundary
def boundaPoints(segs):
	points = []
	if len(segs) == 1:
		# Extract underlaying curve
		for s in segs[0]:
			curve = s.GetCurve()
			point = curve.GetEndPoint(0)
			points.append(point)
		return points

# Function to retrieve centroid
def centroid(points):
	# Retrieve single coordinates
	xCoor = [x[0] for x in points]
	yCoor = [y[1] for y in points]
	zCoor = [z[2] for z in points]
	length = len(points)
	# Retrieve center
	xCenter = sum(xCoor) / length
	yCenter = sum(yCoor) / length
	zCenter = sum(zCoor) / length
	return DB.XYZ(xCenter, yCenter, zCenter)

# Function to retrieve center of room
def roomCenter(room):
	per = room.Perimeter
	return per

# Function to create sheet
def createSheet(room, titleBlockId, prefix = "INTERIOR ELEVATIONS"):
	sheet = DB.ViewSheet.Create(doc, titleBlockId)
	sheet.Name = room.Number + " - " + prefix
	return sheet

# Function to create elevations
def createElev(room, viewTypeId, location, viewTempId):
	viewsId = []
	if room.Location != None:
		marker = DB.ElevationMarker.CreateElevationMarker(doc, viewTypeId, location, 5)
		# Create all views for elevations, integers from 0 to 3
		for intView in range(0,4):
			view = marker.CreateElevation(doc, doc.ActiveView.Id, intView)
			view.ViewTemplateId = viewTempId
			viewsId.append(view.Id)
	return viewsId

# Function to place views on sheets
def placeViews(viewSheetId, ViewId, point):
	DB.Viewport.Create(doc, viewSheetId, ViewId, point)

# Prompt to select rooms
roomsElev = roomElev()
viewTypeId = viewTypeId()
titleBlockId = titleTypeId()
viewTempId = viewTempId()

# Create transaction and start it
t = DB.Transaction(doc, "Create Markers")
t.Start()
# Create elevation markers
for r in roomsElev:
	bounda = boundaries(r)
	points = boundaPoints(bounda)
	center = centroid(points)
	viewsId = createElev(r, viewTypeId, center, viewTempId)
	sheet = createSheet(r, titleBlockId)
	# Place views on sheets
	for v in viewsId:
		placeViews(sheet.Id, v, DB.XYZ(0,0,0))
# Commit transaction
t.Commit()