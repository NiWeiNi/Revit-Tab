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
# Retrieve levels
levels = DB.FilteredElementCollector(doc).OfClass(DB.Level)
levelNames = [x.Name for x in levels]
# Retrieve lines
lines = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Lines)

# Clasify rooms by level name
roomsDict = {}
for r in roomsCollector:
    lvName = r.Level.Name
    if lvName not in roomsDict.keys():
        roomsDict[lvName] = [r]
    else:
        roomsDict[lvName].append(r)

# Function to retrieve rooms by level name
def roomsBylevel(levelName):
    if levelName in roomsDict.keys():
        rooms = roomsDict[lvN]
        return rooms

# Retrieve line to renumber elements
for lvN in levelNames:
    for l in lines:
        if l.LookupParameter("Work Plane") != None:
            wP = l.LookupParameter("Work Plane").AsString()
            lineName = l.LineStyle.Name
            if wP == "Level : " + lvN and lineName == "Room Number Line":
                print l
            