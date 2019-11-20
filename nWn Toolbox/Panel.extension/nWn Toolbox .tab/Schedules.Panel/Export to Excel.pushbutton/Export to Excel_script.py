# -*- coding: utf-8 -*-
"""Export selected schedule to Excel.

NOTE: Only number cells will remain as numbers, elements with text characters will be converted to text.
"""
__author__ = "nWn"
__title__ = "Export\n to Excel"

# Import 
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

# Import xlsxwriter
import xlsxwriter

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Retrieve Schedules
viewsCollector = DB.FilteredElementCollector(doc).OfClass(DB.View)
views = [v for v in viewsCollector if not v.IsTemplate]
schedules = [x for x in views if "<Revision Schedule>".lower() not in x.Name.lower() and x.ViewType == DB.ViewType.Schedule]
schedNames = [x.Name for x in schedules]

# Create form to display schedule to export and retieve schedule
selectedSched = forms.SelectFromList.show(schedNames, button_name="Select Schedule to Export")
sched = [x for x in schedules if x.Name == selectedSched][0]

# Select folder to export excel
destinationFolder = forms.pick_folder()

# Retrieve data from the schedule
tableData = sched.GetTableData()
sectionData = tableData.GetSectionData(DB.SectionType.Body)
numbRows = sectionData.NumberOfRows
numbCols = sectionData.NumberOfColumns

data = []
# Create list with schedule data with rows as second level lists
for i in range(numbRows):
    rows = []
    for j in range(numbCols):
        content = sched.GetCellText(DB.SectionType.Body, i, j)
        rows.append(content)
    data.append(rows)

# Check maximun length of data in columns
lengths = [len(x) for x in data[0]]
for row in data:
    for cell, lng in zip(row, lengths):
        newLength = len(cell)
        if newLength > lng:
            ind = lengths.index(lng)
            lengths[ind] = newLength

# Export data to excel
workbook = xlsxwriter.Workbook(destinationFolder + "\\" + sched.Name + ".xlsx")
worksheet = workbook.add_worksheet()

# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0

# Iterate over the data and write it out row by row.
for item in data:
    for it in item:
        worksheet.write(row, col, it)
        col += 1
    row += 1
    col = 0

workbook.close()