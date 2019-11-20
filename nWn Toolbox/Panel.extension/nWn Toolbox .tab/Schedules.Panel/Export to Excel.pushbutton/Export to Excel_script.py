# -*- coding: utf-8 -*-
"""Export selected schedule to Excel.

NOTE: Only number cells will remain as numbers, elements with text characters will be converted to text.
"""
__author__ = "nWn"
__title__ = "Export\n to Excel"

# Import 
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Retrieve Schedules
viewsCollector = DB.FilteredElementCollector(doc).OfClass(DB.View)
views = [v for v in viewsCollector if not v.IsTemplate]
schedules = [x for x in views if "<Revision Schedule>".lower() not in x.Name.lower() and x.ViewType == DB.ViewType.Schedule]
schedNames = [x.Name for x in schedules]

# Create form to display schedule to export
selectedSched = forms.SelectFromList.show(schedNames, button_name="Select Schedule to Export")



