# -*- coding: utf-8 -*-
"""Number doors according to room number.
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

# Select all doors
doorsFilter = DB.ElementCategoryFilter(DB.BuiltInCategory.OST_Doors)
doorsCollector = DB.FilteredElementCollector(doc).WherePasses(doorsFilter).WhereElementIsNotElementType()

# Select all phases
phases = doc.Phases
phasesName = [ph.Name for ph in phases]

# Class 

# Form to select phase
phaseForm = forms.SelectFromList.show(phasesName, title = "Select Phase")

print phaseForm