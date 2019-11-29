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
    # Check central model path
    modelPath = doc.GetWorksharingCentralModelPath()
    centralPath = DB.ModelPathUtils.ConvertModelPathToUserVisiblePath(modelPath)
    # Check if model is detached or workshared in the local drive
    if doc.IsWorkshared and not centralPath.startswith("C:"):
        return True
    else:
        return False

# Create progress bar
count = 1
finalCount = 0
with forms.ProgressBar(step=10) as pb:

    # Check if model is linked to central
    if checkCentral():
        # Finish execution script if model is not detached
        forms.alert("Please detach model from central and save it to your local drive.", ok = True, exitscript= True)

    # Collect all views and sheets
    viewsCollector = DB.FilteredElementCollector(doc).OfClass(DB.View)
    sheetsCollector = DB.FilteredElementCollector(doc).OfClass(DB.ViewSheet)

    # Select parameter in selected view
    view = None
    for v in viewsCollector:
        if v.ViewType == DB.ViewType.FloorPlan:
            view = v
            break
    param = None
    for p in view.Parameters:
        if "View Set" in p.Definition.Name:
            param = p.Definition.Name
            break
    
    # Set view set to select
    viewSet = [x.LookupParameter(param).AsString() for x in viewsCollector if x.LookupParameter(param) != None]
    selectSet = sorted(set(viewSet))

    # Display select view sets form
    vSet = forms.SelectFromList.show(selectSet, "View Set to Keep", 600, 600, multiselect=True)
    # Exclude start page to be deleted
    vSet.append("START PAGE")

    # Classify views
    viewsIdDelete = [x.Id for x in viewsCollector if x.LookupParameter(param) == None or \
                    x.LookupParameter(param).AsString() not in vSet]
    viewsIdKeep = [x.Id for x in viewsCollector if x.LookupParameter(param) != None and \
                    x.LookupParameter(param).AsString() in vSet]

    # Prompt form to check if user wants to keep annotations
    delAnnotations = forms.alert("Delete annotation elements", title="Delete annotations?", yes=True, no=True)

    # Update progress bar
    pb.update_progress(count, finalCount)
    count += 1

    # Create group transaction
    tg = DB.TransactionGroup(doc, "Delete elements in document")
    # Start group transaction
    tg.Start()

    # Collect annotation categories to be deleted
    annoElements = []

    # Check if annotation elements must be deleted
    if delAnnotations:
        
        # Categories
        categories = doc.Settings.Categories
        # Elements of categories to delete
        catDel = ("Dimensions", "Railing Tags", "Furniture Tags", "Spot Slopes", "Spot Elevations", "Floor Tags", "Door Tags", "Window Tags", "Specialty Equipment Tags", "Material Tags", "Property Line Segment Tags", "Wall Tags", "Parking Tags", "Color Fill Legends", "Spot Elevation Symbols", "Structural Column Tags", "Room Tags", "Generic Model Tags", "Title Blocks", "Text Notes", "Callout Heads", "Structural Foundation Tags", "Lighting Device Tags", "Curtain Panel Tags", "Ceiling Tags", "Generic Annotations", "Plumbing Fixture Tags", "Roof Tags", "Casework Tags", "Revision Clouds", "Reference Planes", "Electrical Fixture Tags")
        # Check elements to delete
        for cat in categories:
            if cat.CategoryType == DB.CategoryType.Annotation:
                collector = DB.FilteredElementCollector(doc).OfCategoryId(cat.Id)
                elemIds = [x.Id for x in collector if x.Category.Name in catDel]
                annoElements = annoElements + elemIds
        # annoIds = List[DB.ElementId](annoElements)
       
    finalCount = len(annoElements + viewsIdDelete)
    
    # Create single transaction and start it
    t = DB.Transaction(doc, "Delete views")
    t.Start()

    for v in viewsIdDelete:
        try:
            doc.Delete(v)
        except:
            pass
        # Update progress bar
        pb.update_progress(count, finalCount)
        count += 1

    # Commit transaction
    t.Commit()

    # Create single transaction and start it
    t1 = DB.Transaction(doc, "Delete annotation elements")
    t1.Start()
    # Delete all annotation elements
    for i in annoElements:
        try:
            doc.Delete(i)
        except:
            pass
        # Update progress bar
        pb.update_progress(count, finalCount)
        count += 1

    # Commit transaction
    t1.Commit()
    # Commit group transaction
    tg.Commit()