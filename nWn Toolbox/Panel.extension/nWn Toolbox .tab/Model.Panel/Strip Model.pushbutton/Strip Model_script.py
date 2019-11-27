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

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Function to check file is not workshared in the server
def checkCentral():
    if forms.check_workshared(doc=revit.doc):
        centralPath = revit.query.get_central_path(doc=revit.doc)
        if centralPath.startswith("C:"):
            return True
        else:
            return False

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

# Create single transaction and start it
t = DB.Transaction(doc, "Delete elements")
t.Start()

for v in viewsIdDelete:
    try:
        doc.Delete(v)
    except:
        pass

# Commit transaction
t.Commit()