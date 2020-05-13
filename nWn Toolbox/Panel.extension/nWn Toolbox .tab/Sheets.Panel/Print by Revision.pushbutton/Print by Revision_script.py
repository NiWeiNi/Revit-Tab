# -*- coding: utf-8 -*-
"""Print all sheets with a specified revision date. 

NOTE: 
Name of the files will be sheet number, name and appended revision.
Existing files will be overwritten."""
__title__ = 'Print by\nRev Date'
__author__ = "nWn"

# Import commom language runtime
import clr
# Import winreg to edit Registry
import _winreg

# Import Revit DB
from pyrevit import forms
from pyrevit import DB

# Import libraries to enable Windows forms
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

from System.Drawing import Point, Size
from System.Windows.Forms import Application, Button, Form, Label, TextBox, FolderBrowserDialog, DialogResult


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
		self.textboxDiv.Text = "Input Revision Date"
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


# Function to set the printing path in the registry
def changePrintPath(printPath):
	try:
		key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, keyValue, 0, _winreg.KEY_ALL_ACCESS)
		originalKeyValue = _winreg.QueryValueEx(key, "AutoSaveDir")
	except:
		pass

	_winreg.SetValueEx(key, "AutoSaveDir", 0, _winreg.REG_SZ, printPath)
	_winreg.CloseKey(key)

# Function to return the the registry to original state
def unmodifyRegistry(keyValue, originalKeyValue):
	try:
		key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, keyValue, 0, _winreg.KEY_ALL_ACCESS)
		_winreg.SetValueEx(key, "AutoSaveDir", 0, _winreg.REG_SZ, originalKeyValue)
		_winreg.CloseKey(key)
	except:
		pass

# Function to create Windows folder browser
def windBrowser():
	# Create folder browser window 
	dialog = FolderBrowserDialog()
	# Record for user action and store selected path
	if (dialog.ShowDialog() == DialogResult.OK):
		return dialog.SelectedPath

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
	viewSet = DB.ViewSet()
	viewSet.Insert(sheet)
	viewSheetSetting = printManager.ViewSheetSetting
	viewSheetSetting.CurrentViewSheetSet.Views = viewSet
	viewSheetSetting.SaveAs("Current Print")

	# Set printer
	printManager.SelectNewPrintDriver(printerName)
	printManager.Apply()

	# Check if printer is virtual and set print to file
	printManager.CombinedFile = combined
	printManager.Apply()
	if printManager.IsVirtual:
		printManager.PrintToFile = True
	else:
		printManager.PrintToFile = False
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

# Function to display results to user
def printMessage(resultList, message, messageWarning):
	if len(resultList) != 0:
		print(message)
		print("\n".join(resultList))
	else:
		print(messageWarning)

""" Start of printing script """
# Global values, predefined parameters
originalKeyValue = ""
keyValue = r"Software\PDFPrint\Services\PDF"
# Variable to store sheets with revisions
sheets = []
# Naming of pdf files
fileNames = []
# Printed and failed sheets
printedSheets = []
failedSheets = []
# Store current document to variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Call windBrowser to select folder
printFolder = windBrowser()

# Call the CreateWindow class and create the input for Revision Date
formRevision = CreateWindow("Revision Date on Sheets to Print", "Input Revision Date")
Application.Run(formRevision)

# Assign the input to variable
revDate = formRevision.value

# Collects all sheets in current document
sheetsCollector = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Sheets)

# Get curent revision on sheets and collect sheets
for s in sheetsCollector:
	"""
	if s.GetCurrentRevision() != DB.ElementId.InvalidElementId and \
		doc.GetElement(s.GetCurrentRevision()).RevisionDate == revDate:
		rev = doc.GetElement(s.GetCurrentRevision())
		"""
	sheets.append(s)

# Retrieve sheets number, name and revision
for s in sheets:
	number = s.SheetNumber
	name = s.Name
	revision = "Alo"
	# revision = s.GetRevisionNumberOnSheet(doc.GetElement(s.GetCurrentRevision()).Id)
	pdfName = printFolder + "\\" + number + " - " + name + "[" + revision + "]" + ".pdf"
	fileNames.append(pdfName)

# Collect all print settings from document
printSettingCollector = DB.FilteredElementCollector(doc).OfClass(DB.PrintSetting)

# Change path to save printed files
changePrintPath(printFolder)

# Create a individual transaction
t = DB.Transaction(doc, "Batch Print")
# Start transaction
t.Start()
for sheet, fileName in zip(sheets, fileNames):
	try:
		printSheet(sheet, "PDF24", True, fileName, "A3")
		printedSheets.append(sheet.SheetNumber)
	except:
		failedSheets.append(fileName)
# Commit transaction
t.Commit()

# Return Registry to original path
unmodifyRegistry(keyValue, originalKeyValue)

# Print message
printMessage(printedSheets, "The following sheets have been printed:", "No file has been printed.") 