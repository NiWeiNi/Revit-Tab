# -*- coding: utf-8 -*-
"""Create worksets from Excel.

NOTE: Excel should contain at least Name of the worksets.
"""
__author__ = "nWn"
__title__ = "Worksets\n from Excel"

# Import 
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

# Import libraries
import clr
clr.AddReference("Microsoft.Office.Interop.Excel")
from Microsoft.Office.Interop import Excel

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Function to retrieve data
def retData(array):
    data = []
    for a in array:
        if a == None:
            break
        else:
            data.append(a)
    return data

# Function to create worksets
def createWorkset(name):
    # Check name is unique and create workset
    if DB.WorksetTable.IsWorksetNameUnique(doc, name):
        workset = DB.Workset.Create(doc, name)

# Function alert and quit
def alert(message):
	return forms.alert(message, ok = True, exitscript= True)

# Function to check if file is workshared
def workshared():
    if doc.IsWorkshared:
        return True
    else:
        return alert("Document is not workshared.")

if workshared():

    # Prompt user to specify file path
    pathFile = forms.pick_file(files_filter='Excel Workbook (*.xlsx)|*.xlsx|''Excel 97-2003 Workbook|*.xls')       

    # Create Excel object
    excel = Excel.ApplicationClass()
    workbook = excel.Workbooks.Open(pathFile)
    ws = workbook.Worksheets[1]

    # Read data
    worksetNames = ws.Range["A1", "A1000"]
    wNames = [str(x) for x in retData(worksetNames.Value2)[1:]]

    # Create progress bar
    count = 1
    finalCount = len(wNames)
    with forms.ProgressBar(step=1) as pb:
        # Create and start transtaction
        t = DB.Transaction(doc, "Create Worksets")
        t.Start()
        # Create worksets
        for name in wNames:
            try:
                createWorkset(name)
            except:
                pass
            # Update progress bar
            pb.update_progress(count, finalCount)
            count += 1

        # Commit transaction
        t.Commit()

    excel.Workbooks.close()
    excel.quit()