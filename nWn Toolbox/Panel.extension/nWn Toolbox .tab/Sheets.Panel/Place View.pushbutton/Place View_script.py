# -*- coding: utf-8 -*-
"""Place current active view in selected sheet.

NOTE: 
Position will be at center of sheet."""
__title__ = 'Current View\non Sheet'
__author__ = "nWn"

# Import 
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

# Store current document to variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Form to select sheet
sheets = forms.select_sheets()

# Retrieve current view
curView = doc.ActiveView

# Create and start transaction
t = DB.Transaction(doc, "Place view on sheets")
t.Start()

# Place current view on selected sheets
for s in sheets:
    DB.Viewport.Create(revit.doc, s.Id, curView.Id, DB.XYZ(1.94882, 1.37795, 0))

# Commit transaction
t.Commit()