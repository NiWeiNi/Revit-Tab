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
import clr
clr.AddReference("Microsoft.Office.Interop.Excel")
from Microsoft.Office.Interop import Excel
from System.Runtime.InteropServices import Marshal

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Prompt user to specify file path
pathFile = forms.pick_file(files_filter='Excel Workbook (*.xlsx)|*.xlsx|''Excel 97-2003 Workbook|*.xls')

# Create Excel object
excel = Excel.ApplicationClass()
excel = Marshal.GetActiveObject("Excel.Application")
workbook = excel.Workbooks.Open(pathFile)
ws = workbook.Worksheets[1]

# Read data
sNumber = ws.Range["A1", "A1000"]
sName = ws.Range["B1", "B1000"]

print sNumber.Value2
print sName.Value2

excel.ActiveWorkbook.Close(False)
Marshal.ReleaseComObject(ws)
Marshal.ReleaseComObject(workbook)
Marshal.ReleaseComObject(excel)

for n in sNumber.Value2:
    print n
