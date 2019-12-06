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

# Function to display select room number
def roomNumber():
	# Collect all rooms
	rooms = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Rooms)
	# Create set of rooms
	roomNumber = [r.LookupParameter("Number").AsString() + "    ---    " + r.LookupParameter("Name").AsString() for r in rooms]
	# Prompt selection list
	return forms.SelectFromList.show(roomNumber, "Rooms to elevate", 600, 600, multiselect = True)

# Prompt to select rooms
roomNumber()