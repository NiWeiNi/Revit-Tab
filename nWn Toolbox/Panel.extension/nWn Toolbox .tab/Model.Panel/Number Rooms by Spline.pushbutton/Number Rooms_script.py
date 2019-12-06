# -*- coding: utf-8 -*-
"""Number rooms that intersects with spline.

NOTE: 
"""
__author__ = "nWn"
__title__ = "Number\n Rooms"

# Import 
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Retrieve all rooms
roomsCollector = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Rooms)
# Dispose not placed and redundant rooms
roomsF = [x for x in roomsCollector if x.Area != 0.0]
# Retrieve levels
levels = DB.FilteredElementCollector(doc).OfClass(DB.Level)
levelNames = [x.Name for x in levels]
# Retrieve lines
lines = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Lines)

# Function to clasify rooms by level name
def roomSorted(roomsCollector):
    roomsDict = {}
    for r in roomsCollector:
        lvName = r.Level.Name
        if lvName not in roomsDict.keys():
            roomsDict[lvName] = [r]
        else:
            roomsDict[lvName].append(r)
    return roomsDict

# Function to retrieve rooms by level name
def roomsBylevel(levelName, rooms):
    if levelName in roomsDict.keys():
        roomsL = rooms[lvN]
        return roomsL

# Function to modify room number
def changeRoomNumber(room, number):
    number = str(number)
    room.LookupParameter("Number").Set(number)

# Function to map number between 0 and 1
def mapNumbers(listConvert):
    listScaled = []
    # Span of list to convert
    convSpan = listConvert[-1] - listConvert[0] * 1.0
    # Convert number into a 0-1 range and append to output list
    for e in listConvert:
        valueScaled = e / convSpan
        listScaled.append(valueScaled)
    return listScaled

# Rooms by level name
roomsDict = roomSorted(roomsF)

# Options for solid intersection
optSol = DB.SolidCurveIntersectionOptions()

# Options for spatial elements
spOpt = DB.SpatialElementBoundaryOptions()

# Retrieve line to renumber elements
interSeg = []
for lvN in levelNames:
    rooms = roomsBylevel(lvN, roomsDict)
    # Check there are rooms in the level
    if rooms != None:
        for l in lines:
            if l.LookupParameter("Work Plane") != None:
                wP = l.LookupParameter("Work Plane").AsString()
                lineName = l.LineStyle.Name
                if wP == "Level : " + lvN and lineName == "Room Number Line":
                    line = l.GeometryCurve
                    print line.IsBound
        # Obtain intersection between room and curve
        numbRooms = len(rooms)
        roomSort = {}
        for r in rooms:
            parMap = mapNumbers(range(0, numbRooms * 4))
            for norParam in parMap:
                # Check if point in curve is inside room
                cPoint = line.Evaluate(norParam, True)
                if r.IsPointInRoom(cPoint):
                    roomSort[norParam] = r
                    break
        # Create single transaction and start it
        t = DB.Transaction(doc, "Renumber Door")
        t.Start()
        
        # Keys sorted
        keySorted = sorted(roomSort.keys())
        # Chnage door parameters
        for k, n in zip(keySorted, range(numbRooms)):
            changeRoomNumber(roomSort[k], n)

        # Commit transaction
        t.Commit()