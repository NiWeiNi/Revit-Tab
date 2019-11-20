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

