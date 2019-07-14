# -*- coding: utf-8 -*-
"""Dimension grids.
"""
__title__ = 'Dimension\nGrids'
__author__ = "nWn"

# Import commom language runtime
import clr
# Import Revit API
from Autodesk.Revit.DB import FilteredElementCollector, ElementCategoryFilter, \
							BuiltInCategory, ReferenceArray, Reference, Transaction, \
							TransactionGroup, FamilySymbol, Structure
# Import Revit API
from Autodesk.Revit.Creation import ItemFactoryBase

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Get current view
view = doc.ActiveView

# Select all grids by filter
gridsFilter = ElementCategoryFilter(BuiltInCategory.OST_Grids)
gridsCollector = FilteredElementCollector(doc).WherePasses(gridsFilter) \
				.WhereElementIsNotElementType()

# Variables to split grids into columns and rows
gridsColumn = ReferenceArray()
gridsRow = ReferenceArray()

# Check grids name and split in groups
for grid in gridsCollector:
	gridName = grid.LookupParameter("Name").AsString()
	if any(char.isdigit() for char in gridName):
		gridsColumn.Append(Reference(grid))
	else:
		gridsRow.Append(Reference(grid))

# Create dimensions
