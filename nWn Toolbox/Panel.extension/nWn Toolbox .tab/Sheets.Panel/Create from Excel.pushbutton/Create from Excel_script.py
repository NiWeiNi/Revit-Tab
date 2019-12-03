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

# Function to retrieve data
def retData(array1, array2):
    data1 = []
    data2 = []
    for a1, a2 in zip(array1, array2):
        # Check that data is not empty
        if a1 == None and a2 ==None:
            break
        else:
            data1.append(a1)
            data2.append(a2)
    sheets = {"sheetNumbers" : data1, "sheetNames" : data2}
    return sheets

# Function to create sheets
def createSheet(number, name, titleBlockId):
    sheet = DB.ViewSheet.Create(doc, titleBlockId)
    sheet.SheetNumber = number
    sheet.Name = name

# Prompt user to specify file path
pathFile = forms.pick_file(files_filter='Excel Workbook (*.xlsx)|*.xlsx|''Excel 97-2003 Workbook|*.xls')       

# Prompt user to select titleblock
titleBlock = forms.select_titleblocks(doc=doc)

# Create Excel object
excel = Excel.ApplicationClass()
excel = Marshal.GetActiveObject("Excel.Application")
workbook = excel.Workbooks.Open(pathFile)
ws = workbook.Worksheets[1]

# Read data
sNumber = ws.Range["A1", "A1000"]
sName = ws.Range["B1", "B1000"]
sheetNumbers = [str(x) for x in retData(sNumber.Value2, sName.Value2)["sheetNumbers"][1:]]
sheetNames = [str(x) for x in retData(sNumber.Value2, sName.Value2)["sheetNames"][1:]]

# Create progress bar
count = 1
finalCount = len(sheetNumbers)
with forms.ProgressBar(step=10) as pb:
    # Create and start transtaction
    t = DB.Transaction(doc, "Create Sheets")
    t.Start()
    # Create sheets
    for sNumb, sNam in zip(sheetNumbers, sheetNames):
        try:
            createSheet(sNumb, sNam, titleBlock)
        except:
            pass
        # Update progress bar
        pb.update_progress(count, finalCount)
        count += 1

    # Commit transaction
    t.Commit()

"""
excel.ActiveWorkbook.Close(False)
Marshal.ReleaseComObject(ws)
Marshal.ReleaseComObject(workbook)
Marshal.ReleaseComObject(excel)
"""
excel.Workbooks.close()
excel.quit()