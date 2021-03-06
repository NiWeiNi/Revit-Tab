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
import System
clr.AddReference("System")
from System.Collections.Generic import List

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Function to check file is not workshared in the server
def checkCentral():
    # Check if model is not workshared
    try:
        # Check central model path
        modelPath = doc.GetWorksharingCentralModelPath()
        centralPath = DB.ModelPathUtils.ConvertModelPathToUserVisiblePath(modelPath)
    except:
        return False
    # Check if model is detached or workshared in the local drive
    if doc.IsWorkshared and not centralPath.startswith("C:"):
        return True
    else:
        return False

# Function to round to ten
def roundNumber(number, multiple):
    remainder = number % multiple
    if remainder != 0:
        addNumber = multiple - remainder
        updatedNumber = addNumber + number 
        return updatedNumber
    else:
        return number

# Function to purge file
def purge():
    purgeGuid = 'e8c63650-70b7-435a-9010-ec97660c1bda'
    purgableElementIds = []
    performanceAdviser = DB.PerformanceAdviser.GetPerformanceAdviser()
    guid = System.Guid(purgeGuid)
    ruleId = None
    allRuleIds = performanceAdviser.GetAllRuleIds()
    for rule in allRuleIds:
        # Finds the PerformanceAdviserRuleId for the purge command
        if str(rule.Guid) == purgeGuid:
            ruleId = rule
    ruleIds = List[DB.PerformanceAdviserRuleId]([ruleId])
    for i in range(3):
        # Purge
        failureMessages = performanceAdviser.ExecuteRules(doc, ruleIds)
        if failureMessages.Count > 0:
            # Retrieves the elements
            purgableElementIds = failureMessages[0].GetFailingElements()
    # Delete elements
    try:
        doc.Delete(purgableElementIds)
    except:
        for e in purgableElementIds:
            try:
                doc.Delete(e)
            except:
                pass

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
    # Collect all imported elements
    linksCollector = DB.FilteredElementCollector(doc).OfClass(DB.ImportInstance)
    revitLinkCollector = DB.FilteredElementCollector(doc).OfClass(DB.RevitLinkType)
    imagesCollector = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_RasterImages)

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

    # Retrieve id of all linked elements
    importedInstancesId = [x.Id for x in linksCollector]
    revitLinksId = [x.Id for x in revitLinkCollector]
    imagesId = [x.Id for x in imagesCollector]

    # Prompt form to check if user wants to keep annotations
    delAnnotations = forms.alert("Delete annotation elements", title="Delete annotations?", yes=True, no=True)

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
        catDel = ("Dimensions", "Railing Tags", "Furniture Tags", "Spot Slopes", "Spot Elevations", "Floor Tags", "Door Tags", "Window Tags", "Specialty Equipment Tags", "Material Tags", "Property Line Segment Tags", "Wall Tags", "Parking Tags", "Color Fill Legends", "Spot Elevation Symbols", "Structural Column Tags", "Room Tags", "Generic Model Tags", "Text Notes", "Callout Heads", "Structural Foundation Tags", "Lighting Device Tags", "Curtain Panel Tags", "Ceiling Tags", "Generic Annotations", "Plumbing Fixture Tags", "Roof Tags", "Casework Tags", "Revision Clouds", "Reference Planes", "Electrical Fixture Tags")
        # Check elements to delete
        for cat in categories:
            if cat.CategoryType == DB.CategoryType.Annotation:
                collector = DB.FilteredElementCollector(doc).OfCategoryId(cat.Id)
                elemIds = [x.Id for x in collector if x.Category.Name in catDel]
                annoElements = annoElements + elemIds
        # annoIds = List[DB.ElementId](annoElements)
    
    # Collect all elemtns to delete
    delElements = annoElements + viewsIdDelete + importedInstancesId + revitLinksId + imagesId
    finalCount = len(delElements)
    
    # Create single transaction and start it
    t = DB.Transaction(doc, "Delete elements")
    t.Start()

    for e in delElements:
        try:
            doc.Delete(e)
        except:
            pass
        # Update progress bar
        pb.update_progress(count, roundNumber(finalCount, 10))
        count += 1

    # Purge file
    # purge()

    # Commit transaction
    t.Commit()
    # Commit group transaction
    tg.Commit()