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

# Function to retrieve titleblock from sheets
def titleBlock(sheet):
    titleBlock = ""
    ele = DB.FilteredElementCollector(doc).OwnedByView(sheet.Id)
    for e in ele:
        if hasattr(e.Category, 'Name') and e.Category.Name == "Title Blocks":
            titleBlock = e
            return titleBlock

# Function to retrieve width and height of titleblock
def size(titleblock):
    height = titleBlock.get_Parameter(DB.BuiltInParameter.SHEET_WIDTH).AsDouble()
    width = titleBlock.get_Parameter(DB.BuiltInParameter.SHEET_HEIGHT).AsDouble()
    return height, width

# Form to select sheet
sheets = forms.select_sheets()

# Retrieve current view
curView = doc.ActiveView

# Create and start transaction
t = DB.Transaction(doc, "Place view on sheets")
t.Start()

# Place current view on selected sheets
for s in sheets:
    titleBlock = titleBlock(s)
    height = size(titleBlock)[0]
    width = size(titleBlock)[1]
    DB.Viewport.Create(revit.doc, s.Id, curView.Id, DB.XYZ(height/2, width/2, 0))

# Commit transaction
t.Commit()