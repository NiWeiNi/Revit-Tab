# -*- coding: utf-8 -*-
"""Dimension grids.
"""
__title__ = 'Dimension\nGrids'
__author__ = "nWn"

# Import 
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

import clr
import System
clr.AddReference("System")
from System.Collections.Generic import List

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Function to check if lineas are parallel
def parallel(gridA, gridB):
	startA = gridA.Curve.GetEndPoint(0)
	startB = gridB.Curve.GetEndPoint(0)
	# Check if vectors are parallel
	crossP = startA.CrossProduct(startB)
	if crossP.X == 0 and crossP.Y == 0:
		return True
	
# Get current view
view = doc.ActiveView

# Select all grids by filter
gridsFilter = DB.ElementCategoryFilter(DB.BuiltInCategory.OST_Grids)
gridsCollector = DB.FilteredElementCollector(doc).WherePasses(gridsFilter).WhereElementIsNotElementType()

# Convert gridsCollector into list and split them into parall
grids = list(gridsCollector)
gridGroups = {}
excludedGrids = []
for grid in grids:
	if grid not in excludedGrids:
		gridName = grid.LookupParameter("Name").AsString()
		gridCurve = grid.Curve
		for g in grids:
			iRA = DB.IntersectionResultArray()
			inter = gridCurve.Intersect(g.Curve)
			if inter == DB.SetComparisonResult.Disjoint:
				print parallel(grid, g)

"""
# Variables to split grids into columns and rows
gridsColumn = DB.ReferenceArray()
gridsRow = DB.ReferenceArray()
gridsC = []
gridsR = []

# Check grids name and split in groups
for grid in gridsCollector:
	gridName = grid.LookupParameter("Name").AsString()
	if any(char.isdigit() for char in gridName):
		gridsColumn.Append(DB.Reference(grid))
		gridsC.append(grid)
	else:
		gridsRow.Append(DB.Reference(grid))
		gridsR.append(grid)

# Retrieve endpoints
endPointC0 = gridsC[0].Curve.GetEndPoint(0)
endPointC1 = gridsC[-1].Curve.GetEndPoint(0)

endPointR0 = gridsR[0].Curve.GetEndPoint(0)
endPointR1 = gridsR[-1].Curve.GetEndPoint(0)

# Create line to place dimension
lineC = DB.Line.CreateBound(endPointC0, endPointC1)
lineR = DB.Line.CreateBound(endPointR0, endPointR1)

# Create transaction to create dimensions
t = DB.Transaction(doc, "Dimension grids")
t.Start()

# Create dimensions
doc.Create.NewDimension(view, lineC, gridsColumn)
doc.Create.NewDimension(view, lineR, gridsRow)

# Commit transaction
t.Commit()
"""