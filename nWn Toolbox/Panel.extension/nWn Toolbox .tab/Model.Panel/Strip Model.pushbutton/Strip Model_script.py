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

# Collect all views and sheets
viewsCollector = DB.FilteredElementCollector(doc).OfClass(DB.View)
sheetsCollector = DB.FilteredElementCollector(doc).OfClass(DB.ViewSheet)

# Select parameter in view
view = [x for x in viewsCollector if x.ViewType == DB.ViewType.FloorPlan][0]
param = [p for p in view.Parameters if "View Set" in p.Definition.Name][0]
