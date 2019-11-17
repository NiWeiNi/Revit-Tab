# -*- coding: utf-8 -*-
"""Removes all unused links.

NOTE: Includes images, CAD Links and Revit Links.
"""
__title__ = 'Clean Unused\nLinks'
__author__ = "nWn"

# Import 
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Collect all imported elements
linksCollector = DB.FilteredElementCollector(doc).OfClass(DB.ImportInstance)
revitLinkCollector = DB.FilteredElementCollector(doc).OfClass(DB.RevitLinkType)
# Helper variables
linksDelete = []
linkSuccess = []
linksFail = []

# Collect all links with external path file
for e in linksCollector:
    if e.IsLinked:
        l = DB.ExternalFileUtils.GetExternalFileReference(doc, e.GetTypeId())
        # Retrieve links that are not Loaded
        status = l.GetLinkedFileStatus()
        if status != DB.LinkedFileStatus.Loaded:
            linksDelete.append(e.Id)

# Check Revit links are loaded
for rLink in revitLinkCollector:
    # Retrieve Ids of not loaded Revit links
    if not rLink.IsLoaded(doc, rLink.Id):
        linksDelete.append(rLink.Id)

# Create a individual transaction to change the parameters on sheet
t = DB.Transaction(doc, "Delete Unloaded Links")
# Start individual transaction
t.Start()

# Loop to delete all links
for linkDel in linksDelete:
    doc.Delete(linkDel)

# Commit individual transaction
t.Commit()

# Print removed links
