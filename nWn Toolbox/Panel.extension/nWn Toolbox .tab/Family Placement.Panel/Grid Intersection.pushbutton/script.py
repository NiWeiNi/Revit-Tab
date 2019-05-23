# -*- coding: utf-8 -*-
"""Place families in the grids intersections.

Note:
Allows placement of any family in the grids intersections."""
__author__ = "nWn"
# Import commom language runtime
import clr

# from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import FilteredElementCollector, ElementCategoryFilter, \
							BuiltInCategory, IntersectionResultArray, Transaction, \
							TransactionGroup, Curve, IntersectionResult, XYZ

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Select all grids by filter
gridsFilter = ElementCategoryFilter(BuiltInCategory.OST_Grids)
gridsCollector = FilteredElementCollector(doc).WherePasses(gridsFilter) \
											.WhereElementIsNotElementType() \
											.ToElements()

# Create IntersectionArray object
interRes = clr.Reference[IntersectionResultArray]()

# Check for intersections
inter = gridsCollector[0].Curve.Intersect(gridsCollector[4].Curve, interRes)


print(interRes.Item[0].XYZPoint)
