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

# Clasify rooms by level name
roomsDict = {}
for r in roomsCollector:
    lvName = r.Level.Name
    if lvName not in roomsDict.keys():
        roomsDict[lvName] = [r]
    else:
        roomsDict[lvName].append(r)