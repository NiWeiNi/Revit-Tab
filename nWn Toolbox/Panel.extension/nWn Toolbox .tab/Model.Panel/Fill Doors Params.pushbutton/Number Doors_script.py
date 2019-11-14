# -*- coding: utf-8 -*-
"""Select doors in rooms and fill in parameters.

NOTE: 
"""
__author__ = "nWn"
__title__ = "Fill Doors\n Params"

# Import 
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Select all doors
doorsFilter = DB.ElementCategoryFilter(DB.BuiltInCategory.OST_Doors)
doorsCollector = DB.FilteredElementCollector(doc).WherePasses(doorsFilter).WhereElementIsNotElementType().ToElements()

# Create set of Room Name
roomNames = sorted(list(set([d.LookupParameter("Room Name").AsString() for d in doorsCollector])))

# Create form to select doors by Room Name
roomNameDoors = forms.SelectFromList.show(roomNames, "View Templates", 600, 300, multiselect=True)
