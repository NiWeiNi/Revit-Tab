# -*- coding: utf-8 -*-
"""Create sheets from Excel.

NOTE: Excel should contain at least Number of the sheets.
"""
__author__ = "nWn"
__title__ = "Create\n from Excel"

# Import 
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

# Import libraries
import xlsxwriter

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
