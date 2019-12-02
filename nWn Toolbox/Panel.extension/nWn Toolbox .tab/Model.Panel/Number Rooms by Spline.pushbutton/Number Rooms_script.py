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
