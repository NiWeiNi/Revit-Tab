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

