# -*- coding: utf-8 -*-
"""Places elements along a curve.

NOTE: The division will be in equal parts.
"""
__title__ = 'Matrix\nCurve'
__author__ = "nWn"

# Import commom language runtime
import clr

# Import math module
import math

# Import Revit UI
from Autodesk.Revit.UI.Selection import ObjectType, ISelectionFilter
from Autodesk.Revit.UI import TaskDialog

# Import 
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

# Import modules to create windows dialogues in Revit for user input
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.Windows.Forms import *
from System.Drawing import *

# Store current document to variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Dialog in Revit document to instruct user
TaskDialog.Show("Isolated Selection", "Pick curve for matrix path")

# Define class to filter elements of category to select 
class CustomSelectionFilter(ISelectionFilter):
	def __init__(self, category):
		self.category = category
	def AllowElement(self, e):
		if e.Category.Id == DB.Category.GetCategory(doc, self.category).Id:
			return True
		else:
			return False
	def AllowReference(self, ref, point):
		return True

# Select curve
objType = ObjectType.Element
customFilter = CustomSelectionFilter(DB.BuiltInCategory.OST_Lines)
selCurve = uidoc.Selection.PickObjects(objType, customFilter, "Pick curve for matrix path")

# Convert the reference element into a geometry curve
curve = doc.GetElement(selCurve[0].ElementId).GeometryCurve

# Tessellate curve to get points
tesseCurve = curve.Tessellate()

# Retrieve end point of curve
endPoint = curve.GetEndPoint(0)

# List to store division points
finalPoints = []
stepsize = 50
dist = 0

# Create equal distance points
for p in tesseCurve:
	if len(finalPoints) == 0:
		finalPoints.append(endPoint)
	else:
		dist += endPoint.DistanceTo(p)
		if dist > stepsize:
			finalPoints.append(p)
			dist = 0
		endPoint = p

# Retrieve family to place on points
markingSymbol = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_GenericModel)
markingSymbol.OfClass(FamilySymbol).ToElements()

cogSymbol = markingSymbol.FirstElement()
for element in markingSymbol:
	if element.FamilyName == "CoG":
		cogSymbol = element

# Create a individual transaction
t = Transaction(doc, "Divide curve")
# Start individual transaction
t.Start()

for p in finalPoints:
	doc.Create.NewFamilyInstance(p, cogSymbol, Structure.StructuralType.NonStructural)

# Commit transaction
t.Commit()