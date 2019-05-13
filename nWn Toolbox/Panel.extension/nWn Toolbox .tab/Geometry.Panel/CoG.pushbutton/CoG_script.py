# -*- coding: utf-8 -*-
"""Place a 3D symbol in the center of gravity of the selected element.

Note: the 3D symbol will be added in the assembly"""
__author__ = "nWn"

# Import commom language runtime
import clr

clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName("PresentationFramework")
clr.AddReferenceByPartialName('System')
clr.AddReferenceByPartialName('System.Windows.Forms')

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Pick model curve in Revit document to place elements
# Code based on john pierson´s isolated select model elements node
TaskDialog.Show("Isolated Selection", "Pick curve to follow path")

sel1 = uidoc.Selection
obt1 = Selection.ObjectType.Element

# Define class to filter elements of category to select 
class CustomISelectionFilter(Selection.ISelectionFilter):
	def __init__(self, nom_categorie):
		self.nom_categorie = nom_categorie
	def AllowElement(self, e):
		if e.Category.Name == self.nom_categorie:
			return True
		else:
			return False
	def AllowReference(self, ref, point):
		return true

el_ref = sel1.PickObject(obt1, CustomISelectionFilter("Walls"))
		
# Stores the selected modelcurve into curve, marks it as Revit owned element and extracts geometry
element = SpatialElementGeometryCalculator(doc).CalculateSpatialElementGeometry(el_ref)
