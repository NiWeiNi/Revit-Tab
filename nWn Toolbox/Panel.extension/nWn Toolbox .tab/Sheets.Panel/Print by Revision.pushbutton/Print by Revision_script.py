# -*- coding: utf-8 -*-
"""Print all sheets with a specified revision date. 

NOTE: 
Name of the files will be sheet number, name and appended revision.
Existing files will be overwritten."""
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
from System.Windows.Forms import Application, Button, Form, Label, TextBox, FolderBrowserDialog, DialogResult

# Import os, shutil to move files
import os, shutil

# Import sleep for moving files after printing
from time import sleep

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
		self.textboxDiv.Text = "01/22/2019"
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

# Path to save the pdfs by default
directory = "C:\Users\Snoopy\Desktop"

# Function to create Windows folder browser
def windBrowser():
    # Create folder browser window 
    dialog = FolderBrowserDialog()
    # Record for user action and store selected path
    if (dialog.ShowDialog() == DialogResult.OK):
        return dialog.SelectedPath

# Call windBrowser to select folder with backup files and store path to var
finalDirectory = windBrowser()

# Call the CreateWindow class and create the input for Revision Date
formRevision = CreateWindow("Revision Date on Sheets to Print", "Input Revision Date")
Application.Run(formRevision)

# Assign the input to variable
revDate = formRevision.value

# Store current document to variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Collects all sheets in current document
sheetsCollector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets)

# Variable to store sheets with revisions
sheets = []

# Get curent revision on sheets and collect sheets
for s in sheetsCollector:
	if s.GetCurrentRevision() != ElementId.InvalidElementId and doc.GetElement(s.GetCurrentRevision()).RevisionDate == revDate:
		rev = doc.GetElement(s.GetCurrentRevision())
		sheets.append(s)

# Retrieve sheets number, name and revision
outName = []
finalName = []
for s in sheets:
	number = s.SheetNumber
	name = s.Name
	revision = s.GetRevisionNumberOnSheet(doc.GetElement(s.GetCurrentRevision()).Id)
	pdfName = directory + "\\" + number + " - " + name + "[" + revision + "]" + ".pdf"
	finalPdfName = finalDirectory + "\\" + number + " - " + name + "[" + revision + "]" + ".pdf"
	outName.append(pdfName)
	finalName.append(finalPdfName)

# Check if there are files with same name and clean them
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

# Function to print
def printSheet(sheet, printerName, combined, filePath, printSettingName):

	# Set print range
	printManager = doc.PrintManager
	printManager.PrintRange = printManager.PrintRange.Select
	printManager.Apply()

	# Define current view set as current
	viewSet = ViewSet()
	viewSet.Insert(sheet)
	viewSheetSetting = printManager.ViewSheetSetting
	viewSheetSetting.CurrentViewSheetSet.Views = viewSet
	viewSheetSetting.SaveAs("Current Print")

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

	# Delete Current viewSheetSettings to allow new setting to be stored
	viewSheetSetting.Delete()

# Create a Transaction group to group all subsequent transactions
tg = TransactionGroup(doc, "Batch Print")
# Start the group transaction
tg.Start()

# Create a individual transaction
t = Transaction(doc, "Print")
# Start transaction
t.Start()

# Print sheets
printedSheets = []
failedSheets = []
for sheet, fileName in zip(sheets, outName):
	try:
		printSheet(sheet, "PDF24", True, fileName, "A3")
		printedSheets.append(sheet.Name)
	except:
		failedSheets.append(fileName)

# Commit transaction
t.Commit()

# Combine all individual transaction in the group transaction
tg.Assimilate()

# Function to Move Files
def moveFiles(origin, destination):
	for fileName, finalDestination in zip(outName, finalName):
		shutil.move(fileName, finalDestination)

# Set timer to call function and Move files to final destination
timeToPrint = 4
sleep(len(outName) * timeToPrint)
moveFiles(outName, finalName)

# Function to display result to user
def printMessage(resultList, message, messageWarning):
    if len(resultList) != 0:
        print(message)
        print("\n".join(resultList))
    else:
        print(messageWarning)

# Print message
printMessage(printedSheets, "The following sheets have been pdf:", "No file has been pdf.") 