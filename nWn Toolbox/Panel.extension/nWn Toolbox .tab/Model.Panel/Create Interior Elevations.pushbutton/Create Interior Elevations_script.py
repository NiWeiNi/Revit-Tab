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

# Function to display select room
def roomElev():
	# Collect all rooms
	rooms = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Rooms)
	# Create set of rooms
	roomNumber = sorted([RoomsForm(x) for x in rooms], key=lambda x: x.Number)
	# Prompt selection list
	return forms.SelectFromList.show(roomNumber, "Rooms to Elevate", 600, 600, multiselect = True)

def roomCenter(room):
	per = room.Perimeter
	return per

# Prompt to select rooms
roomsElev = roomElev()