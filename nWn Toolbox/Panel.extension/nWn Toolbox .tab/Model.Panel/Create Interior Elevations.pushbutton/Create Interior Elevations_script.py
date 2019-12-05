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