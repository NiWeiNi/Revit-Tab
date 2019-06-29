# -*- coding: utf-8 -*-
"""Places elements along a curve.

NOTE: The division will be in equal parts.
"""
__title__ = 'Remove Unused\nLinks'
__author__ = "nWn"

# Import commom language runtime
import clr

# Import math module
import math

# Import Revit UI
from Autodesk.Revit.UI.Selection import ObjectType, ISelectionFilter
from Autodesk.Revit.UI import TaskDialog

# Import Revit DB
from Autodesk.Revit.DB import FilteredElementCollector, ImportInstance, BuiltInCategory, \
                            Transaction, TransactionGroup

# Import modules to create windows dialogues in Revit for user input
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.Windows.Forms import *
from System.Drawing import *

# Store current document to variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Dialog in Revit document to instruct user
TaskDialog.Show("Isolated Selection", "Pick curve for path of matrix")

# Define class to filter elements of category to select 
class CustomISelectionFilter(ISelectionFilter):
	def __init__(self, categorie):
		self.categorie = categorie
	def AllowElement(self, e):
		if e.Category.Name == self.categorie:
			return True
		else:
			return False
	def AllowReference(self, ref, point):
		return True

# Select curve
objType = ObjectType.Element
selCurve = uidoc.Selection.PickObjects(objType, "Pick elements to isolate with transparency")

# Convert the reference element into a curve
curve = doc.GetElement(selCurve[0].ElementId)
print curve