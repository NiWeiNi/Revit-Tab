# -*- coding: utf-8 -*-
"""Create views with harcoded view templates for all assemblies of a specific type.

NOTE: The views are harcoded and must be changed per project basis."""
__title__ = 'Create\nViews'
__author__ = "nWn"
# Import commom language runtime
import clr

# Import Revit API
from Autodesk.Revit.DB import FilteredElementCollector, ElementClassFilter, ElementCategoryFilter, \
							Transaction, AssemblyInstance, AssemblyViewUtils, AssemblyDetailViewOrientation			

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Filter to select assemblies
assFilter = ElementClassFilter(AssemblyInstance)

# Select all assemblies in project
assembliesFilter = FilteredElementCollector(doc).WherePasses(assFilter).ToElementIds()

# Create a individual transaction
t = Transaction(doc, "Create Assembly Views")

# Start new transaction to create views
t.Start()

# Create 3D View
for asseId in assembliesFilter:
	AssemblyViewUtils.Create3DOrthographic(doc, asseId)
# Create Elevation Front
	AssemblyViewUtils.CreateDetailSection(doc, asseId, AssemblyDetailViewOrientation.ElevationFront)
# Create Detail Section A
	AssemblyViewUtils.CreateDetailSection(doc, asseId, AssemblyDetailViewOrientation.DetailSectionA)

# Commit individual transaction
t.Commit()