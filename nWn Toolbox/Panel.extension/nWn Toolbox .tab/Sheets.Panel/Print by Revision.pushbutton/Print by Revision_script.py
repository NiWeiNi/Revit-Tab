# -*- coding: utf-8 -*-
"""Print all sheets with a specified revision date. 

NOTE: 
Name of the files will be sheet name and appended revision.
Existing files will be overridden."""
__title__ = 'Print by\nRev Date'
__author__ = "nWn"

# Import commom language runtime
import clr

# Import Revit DB
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, \
                            Transaction, TransactionGroup, ElementId, PrintManager, \
							PrintSetting, ViewSet

# Import libraries to enable Windows forms
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

from System.Drawing import Point, Size
from System.Windows.Forms import Application, Button, Form, Label, TextBox

# Import os
import os

"""
# Create a class form
class CreateWindow(Form):
	def __init__(self, title, author):
		# Create the form
		self.Name = "Create Window"
		self.Text = title
		self.Size = Size(500, 150)
		self.CenterToScreen()
		
		self.value = ""
		
		# Create label for input title
		labelDiv = Label(Text = author + ":")
		labelDiv.Parent = self
		labelDiv.Size = Size(100, 150)
		labelDiv.Location = Point(30, 20)
		
		# Create TextBox for input
		self.textboxDiv = TextBox()
		self.textboxDiv.Parent = self
		self.textboxDiv.Text = "Name"
		self.textboxDiv.Location = Point(300, 20)
	
		# Create button
		button = Button()
		button.Parent = self
		button.Text = "Ok"
		button.Location = Point(300, 60)
		
		# Register event
		button.Click += self.ButtonClicked
		
	def ButtonClicked(self, sender, args):
		if sender.Click:
			# Handle non numeric cases
			try:
				self.value = self.textboxDiv.Text
				self.Close()
			except:
				self.Close()

# Call the CreateWindow class and create the input for Drawer
formDrawer = CreateWindow("Change Parameter Drawn By", "Drawn by")
Application.Run(formDrawer)

# Assign the input to variable
nameDrawer = formDrawer.value

# Call the CreateWindow class and create the input for Checker
formChecker = CreateWindow("Change Parameter Checked By", "Checked by")
Application.Run(formChecker)

# Assign the input to variable
nameChecker = formChecker.value

"""
# Store current document to variable
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Path to ssave the pdfs
directory = "C:\Users\Snoopy\Desktop"

# Collects all sheets in current document
sheetsCollector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets)

# Revision date to print
revDate = "Date 1"

# Variable to store sheets with revisions
sheets = []

# Get curent revision on sheets and collect sheets
for s in sheetsCollector:
	if s.GetCurrentRevision() != ElementId.InvalidElementId and doc.GetElement(s.GetCurrentRevision()).RevisionDate == revDate:
		rev = doc.GetElement(s.GetCurrentRevision())
		sheets.append(s)

# Retrieve sheets number, name and revision
outName = []
for s in sheets:
	number = s.SheetNumber
	name = s.Name
	revision = s.GetRevisionNumberOnSheet(doc.GetElement(s.GetCurrentRevision()).Id)
	pdfName = directory + "\\" + number + " - " + name + "[" + revision + "]" + ".pdf"
	outName.append(pdfName)

# Check if there is files with same name and clean them
for file in outName:
	if os.path.exists(file):
		os.remove(file)

# Collect all print settings from document
printSettingCollector = FilteredElementCollector(doc).OfClass(PrintSetting)

# Function to pick printSetting by Name
def pickPrintSetting(name):
	for p in printSettingCollector:
		if p.Name == name:
			return p

# Create ViewSet
viewSet = ViewSet()
#for sheet in sheets:
	#viewSet.Insert(sheet)

# Function to print
def printSheet(viewSet, printerName, combined, filePath, printSettingName):

	# Set print range
	printManager = doc.PrintManager
	printManager.PrintRange = printManager.PrintRange.Select
	printManager.Apply()

	# Define current view set as current
	viewSheetSetting = printManager.ViewSheetSetting
	viewSheetSetting.CurrentViewSheetSet.Views = viewSet
	#viewSheetSetting.SaveAs("MyViewSet")

	# Set printer
	printManager.SelectNewPrintDriver(printerName)
	printManager.Apply()

	# Print to file
	printManager.CombinedFile = combined
	printManager.Apply()
	printManager.PrintToFile = True
	printManager.Apply()

	# Set destination filepath
	printManager.PrintToFileName = filePath
	printManager.Apply()

	# Set print setting
	printSetup = printManager.PrintSetup
	printSetup.CurrentPrintSetting = pickPrintSetting(printSettingName)
	printManager.Apply()

	# Submit to printer
	printManager.SubmitPrint()

# Create a Transaction group to group all subsequent transactions
tg = TransactionGroup(doc, "Update Drawn By and Checked By")
# Start the group transaction
tg.Start()

# Create a individual transaction
t = Transaction(doc, "Print")
# Start transaction
t.Start()

# Print sheets
printedSheets = []
failedSheets = []
i = 0
for sheet, fileName in zip(sheets, outName):
	viewSet = ViewSet()
	viewSet.Insert(sheet)
	try:
		printSheet(viewSet, "PDF24", True, fileName , "A1")
		printedSheets.append(sheet)
		print sheet.Name
		for v in viewSet:
			print v.Name
	except:
		failedSheets.append(sheet)
	i += 1

# Commit transaction
t.Commit()

# Combine all individual transaction in the group transaction
tg.Assimilate()

# Print all printed sheets