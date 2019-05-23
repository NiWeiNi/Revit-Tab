# -*- coding: utf-8 -*-
"""Place a 3D symbol in the center of gravity of the selected element.

Note: 
Select the element/s before executing the script. 
The CoG is approximate."""
__author__ = "nWn"

# Import commom language runtime
import clr

clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName("PresentationFramework")
clr.AddReferenceByPartialName('System')
clr.AddReferenceByPartialName('System.Windows.Forms')

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.Creation import *

app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

from operator import itemgetter, attrgetter, methodcaller
import System

"""
# selection = [ doc.GetElement( elId ) for elId in __revit__.ActiveUIDocument.Selection.GetElementIds() ]

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

opt = Options()
a = doc.GetElement(el_ref)
print(dir(a))


"""
# Create a individual transaction to start changes in Revit database
t = Transaction(doc, "Place CoG Symbol")
# Start transaction
t.Start()

# Select family to place as CoG
markingSymbol = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericModel)
markingSymbol.OfClass(FamilySymbol).ToElements()

cogSymbol = markingSymbol.FirstElement()
for element in markingSymbol:
	if element.FamilyName == "CoG":
		cogSymbol = element



selection = [doc.GetElement( elId ) for elId in __revit__.ActiveUIDocument.Selection.GetElementIds()]

# Store list of CoG
cogLst = list()

opt = Options()

for i in selection:
	geo = i.get_Geometry(opt)
	for a in geo:
		geo = a.ComputeCentroid()
		cogLst.append(geo)

# Place CoG symbols
for cog in cogLst:
	cogPlaced = doc.Create.NewFamilyInstance(cog, cogSymbol, Structure.StructuralType.NonStructural)

# End transaction
t.Commit()