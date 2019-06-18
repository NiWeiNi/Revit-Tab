# -*- coding: utf-8 -*-
"""Place families in the grids intersections.

Note:
Allows placement of any family in the grids intersections."""
__title__ = 'At Grids\nIntersection'
__author__ = "nWn"
# Import commom language runtime
import clr
# from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import FilteredElementCollector, ElementCategoryFilter, \
							BuiltInCategory, IntersectionResultArray, Transaction, \
							TransactionGroup, FamilySymbol, Structure

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Select all grids by filter
gridsFilter = ElementCategoryFilter(BuiltInCategory.OST_Grids)
gridsCollector = FilteredElementCollector(doc).WherePasses(gridsFilter) \
				.WhereElementIsNotElementType()

for g in gridsCollector:
	print(g)
# Variables to split grids into columns and rows
gridsColumn = []
gridsRow = []

# Check grids name
for grid in gridsCollector:
	gridName = grid.LookupParameter("Name").AsString()
	if any(char.isdigit() for char in gridName):
		gridsColumn.append(grid)
	else:
		gridsRow.append(grid)

# Variables to store grids Name and intersection points
gridsPair = []
gridsIntersection = []

# Create IntersectionArray object
interRes = clr.Reference[IntersectionResultArray]()

# Check for intersections and append grids names as pairs and intersection points
for gC in gridsColumn:
	for gR in gridsRow:
		inter = gC.Curve.Intersect(gR.Curve, interRes)
		gCName = gC.LookupParameter("Name").AsString()
		gRName = gR.LookupParameter("Name").AsString()
		gridsPair.append((gCName, gRName))
		gridsIntersection.append(interRes.Item[0].XYZPoint)

# Select family to place in intersections
markingSymbol = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericModel)
markingSymbol.OfClass(FamilySymbol).ToElements()

familyToPlace = markingSymbol.FirstElement()
for element in markingSymbol:
	if element.FamilyName == "CoG":
		cogSymbol = element

# Place families in the intersection grids
for point in gridsIntersection:
	familyPlaced = doc.Create.NewFamilyInstance(point, familyToPlace, Structure.StructuralType.NonStructural)

print(gridsIntersection)
