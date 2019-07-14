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
							TransactionGroup, Line
# Import Revit API
from Autodesk.Revit.Creation.ItemFactoryBase import NewDimension

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
gridsC = []
gridsR = []

# Check grids name and split in groups
for grid in gridsCollector:
	gridName = grid.LookupParameter("Name").AsString()
	if any(char.isdigit() for char in gridName):
		gridsColumn.Append(Reference(grid))
		gridsC.append(grid)
	else:
		gridsRow.Append(Reference(grid))
		gridsR.append(grid)

# Retrieve endpoints
endPointC0 = gridsC[0].Curve.GetEndPoint(0)
endPointC1 = gridsC[-1].Curve.GetEndPoint(0)

endPointR0 = gridsR[0].Curve.GetEndPoint(0)
endPointR1 = gridsR[-1].Curve.GetEndPoint(0)

# Create line to place dimension
lineC = Line.CreateBound(endPointC0, endPointC1)
lineR = Line.CreateBound(endPointR0, endPointR1)

# Create transaction to create dimensions
t = Transaction(doc, "Dimension grids")
t.Start()

# Create dimensions
doc.Create.NewDimension(view, lineC, gridsColumn)
doc.Create.NewDimension(view, lineR, gridsRow)

# Commit transaction
t.Commit()