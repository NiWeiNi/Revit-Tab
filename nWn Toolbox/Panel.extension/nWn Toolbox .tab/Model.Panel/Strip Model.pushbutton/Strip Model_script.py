# -*- coding: utf-8 -*-
"""Strip model except selected views and sheets and purge it .

NOTE:
"""
__author__ = "nWn"
__title__ = "Strip\n Model"

# Import 
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

import clr
clr.AddReference("System")
from System.Collections.Generic import List

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Function to check file is not workshared in the server
def checkCentral():
    if doc.IsWorkshared:
        return True
    else:
        return False

# Check if model is linked to central
if checkCentral():
    # Finish execution script if model is not detached
    forms.alert("Please detach model from central and save it to your local drive.", ok = True, exitscript= True)

# Collect all views and sheets
viewsCollector = DB.FilteredElementCollector(doc).OfClass(DB.View)
sheetsCollector = DB.FilteredElementCollector(doc).OfClass(DB.ViewSheet)

# Select parameter in view
view = [x for x in viewsCollector if x.ViewType == DB.ViewType.FloorPlan][0]
param = [p.Definition.Name for p in view.Parameters if "View Set" in p.Definition.Name][0]

# Set view set to select
viewSet = [x.LookupParameter(param).AsString() for x in viewsCollector if x.LookupParameter(param) != None]
selectSet = sorted(set(viewSet))

# Display select view sets form
vSet = forms.SelectFromList.show(selectSet, "View Set to Keep", 600, 600, multiselect=True)

# Classify views
viewsIdDelete = [x.Id for x in viewsCollector if x.LookupParameter(param) == None or \
                x.LookupParameter(param).AsString() not in vSet]
viewsIdKeep = [x.Id for x in viewsCollector if x.LookupParameter(param) != None and \
                x.LookupParameter(param).AsString() in vSet]

# Prompt form to check if user wants to keep annotations
delAnnotations = forms.alert("Confirm to delete annotation elements", title="Delete annotations?", yes=True, no=True)

# Create group transaction
tg = DB.TransactionGroup(doc, "Delete elements in document")
# Start group transaction
tg.Start()
# Create single transaction and start it
t = DB.Transaction(doc, "Delete views")
t.Start()

for v in viewsIdDelete:
    try:
        doc.Delete(v)
    except:
        pass

# Commit transaction
t.Commit()

# Check if annotation elements must be deleted
if delAnnotations:
    # Collect annotation categories to be deleted
    annoElements = []
    categories = doc.Settings.Categories
    for cat in categories:
        if cat.CategoryType == DB.CategoryType.Annotation:
            collector = DB.FilteredElementCollector(doc).OfCategoryId(cat.Id)
            elemIds = [x.Id for x in collector]
            annoElements = annoElements + elemIds
    annoIds = List[DB.ElementId](annoElements)
    print annoIds

# Create single transaction and start it
t1 = DB.Transaction(doc, "Delete annotation elements")
t1.Start()

# Delete all annotation elements
try:
    doc.Delete(annoIds)
except:
    pass

# Commit transaction
t1.Commit()
# Commit group transaction
tg.Commit()