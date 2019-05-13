# -*- coding: utf-8 -*-
"""Fills in the empty Drawn by parameter after asking for input."""
__author__ = "nWn"

# Import commom language runtime
import clr

clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName("PresentationFramework")
clr.AddReferenceByPartialName('System')
clr.AddReferenceByPartialName('System.Windows.Forms')

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction

app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Collects all sheets in current document
sheetsCollector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets) \
                                                .WhereElementIsNotElementType() \
                                                .ToElements()

tg = Transactiongroup(doc, "Update")

t = Transaction(doc, "Change sheets name")
t.Start()

for sheet in sheetsCollector:
    sheetName = sheet.LookupParameter("Sheet Name")
    if sheetName:
        sheetName.Set("Hello")
        print(sheet.UniqueId)

t.Commit()

tg.Assimilate()