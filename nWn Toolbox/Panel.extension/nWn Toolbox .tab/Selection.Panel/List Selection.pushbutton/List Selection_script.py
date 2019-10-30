# -*- coding: utf-8 -*-
"""List all currently selected elements.
"""
__title__ = 'List\nSelection'
__author__ = "nWn"

# Import 
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
