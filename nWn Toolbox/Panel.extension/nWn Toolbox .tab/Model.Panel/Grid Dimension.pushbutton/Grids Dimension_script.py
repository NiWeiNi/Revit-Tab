# -*- coding: utf-8 -*-
"""Dimension grids.
"""
__title__ = 'Dimension\nGrids'
__author__ = "nWn"

# Import 
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Function to check gradient
def gradient(grid):
	gr = None
	start = grid.Curve.GetEndPoint(0)
	end = grid.Curve.GetEndPoint(1)
	if round(start.X, 10) != round(end.X, 10):
		gr = round((1.0 / (start.X - end.X)) * (start.Y - end.Y), 10)
	return gr

# Function to check if lineas are parallel
def parallel(gridA, gridB):
	return gradient(gridA) == gradient(gridB)

# Function to create ReferenceArray
def refArray(listConv):
	refArray = DB.ReferenceArray()
	for e in listConv:
		refArray.Append(DB.Reference(e))
	return refArray

# Function to create reference line for dimension
def refLine(grids):
	start = grids[0].Curve.GetEndPoint(0)
	end = grids[1].Curve.GetEndPoint(0)
	line = DB.Line.CreateBound(start, end)
	return line
	
# Get current view
view = doc.ActiveView

# Select all grids by filter
gridsFilter = DB.ElementCategoryFilter(DB.BuiltInCategory.OST_Grids)
gridsCollector = DB.FilteredElementCollector(doc).WherePasses(gridsFilter).WhereElementIsNotElementType()

# Convert gridsCollector into list and split them into parallel groups
grids = list(gridsCollector)
gridGroups = {}
excludedGrids = []
# Loop through all grids
for grid in grids:
	gridName = grid.LookupParameter("Name").AsString()
	gridCurve = grid.Curve
	# Check if grid is already classified
	if gridName not in excludedGrids:
		# Check if the rest of the grids are parallel 
		for g in grids:
			inter = gridCurve.Intersect(g.Curve)
			gName = g.LookupParameter("Name").AsString()
			# Check parallel grids and group them
			if gName not in excludedGrids and inter == DB.SetComparisonResult.Disjoint and parallel(grid, g):
				if gridName not in gridGroups.keys():
					gridGroups[gridName] = [grid]
					excludedGrids.append(gridName)
				gridGroups[gridName].append(g)
				excludedGrids.append(gName)

# Create transaction to create dimensions
t = DB.Transaction(doc, "Dimension grids")
t.Start()

for k in gridGroups.keys():
	lt = gridGroups[k]
	line = refLine(lt)
	ref = refArray(lt)
	try:
		# Create dimensions
		doc.Create.NewDimension(view, line, ref)
	except:
		pass

# Commit transaction
t.Commit()