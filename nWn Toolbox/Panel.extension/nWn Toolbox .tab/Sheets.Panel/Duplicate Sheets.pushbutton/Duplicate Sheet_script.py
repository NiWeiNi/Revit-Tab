# -*- coding: utf-8 -*-
"""Duplicate selected sheets.
"""
__title__ = 'Duplicate\n Sheet'
__author__ = "nWn"

# Import 
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Collects all sheets in current document
sheetsCollector = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Sheets)
sheets = [s for s in sheetsCollector if s.IsPlaceholder == False]


