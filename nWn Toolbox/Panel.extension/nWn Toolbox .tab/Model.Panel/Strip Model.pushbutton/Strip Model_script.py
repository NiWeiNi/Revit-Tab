# -*- coding: utf-8 -*-
"""Strip model except selected views and sheets and purge it .

NOTE:
"""
__author__ = "nWn"
__title__ = "Strip\n Model"

# Import 
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument