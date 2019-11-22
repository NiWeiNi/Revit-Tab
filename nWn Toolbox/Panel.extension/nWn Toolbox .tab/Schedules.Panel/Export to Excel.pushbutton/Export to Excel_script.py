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

# Import libraries
import xlsxwriter
from datetime import datetime

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Retrieve date
now = datetime.now()
date = now.strftime("%Y-%m-%d")

# Retrieve project number
projNumber = doc.ProjectInformation.Number

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
filePath = destinationFolder + "\\" + projNumber + "_" + sched.Name + "_" + date + ".xlsx"
workbook = xlsxwriter.Workbook(filePath)
worksheet = workbook.add_worksheet(sched.Name)

# Define format for cells
fontSize = 12
fillColor = "navy"
titleFormat = workbook.add_format({"bold": True, "font_size": fontSize})
subtitleFormat = workbook.add_format({"bg_color": fillColor, "bold": True, 'font_color': "white", "font_size": fontSize})
cellFormat = workbook.add_format({"font_size": fontSize})

# Set columns width
for le, i in zip(lengths, range(len(lengths))):
    worksheet.set_column(i, i, le)

# Start from the first cell. Rows and columns are zero indexed.
row = 1
col = 0

# Set title of schedule
worksheet.write(0, 0, sched.Name.upper(), titleFormat)

# Iterate over the data and write it out row by row.
for item in data:
    first, rest = item[0], item[1:]
    for it in item:
        if (first != "" and rest.count("") == len(lengths)-1) or item.count("") == len(lengths):
            worksheet.write(row, col, it, subtitleFormat)
        elif row == 1:
            worksheet.write(row, col, it, titleFormat)
        else:
            worksheet.write(row, col, it, cellFormat)
        col += 1
    row += 1
    col = 0

workbook.close()