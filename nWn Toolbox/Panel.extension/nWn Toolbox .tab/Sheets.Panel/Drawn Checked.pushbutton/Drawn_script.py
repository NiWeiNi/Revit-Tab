# -*- coding: utf-8 -*-
"""Fills in empty Drawn and Checked parameters with custom input.

NOTE: It will not overrride already filled in parameters."""
__author__ = "nWn"

# Import commom language runtime
import clr

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, \
         Transaction, TransactionGroup

# Import libraries to enable Windows forms
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

from System.Windows.Forms import *
from System.Drawing import *

from System.Drawing import Point
from System.Windows.Forms import Application, Button, Form, Label, TextBox

# Create a class form
class CreateWindow(Form):
	def __init__(self, title, author):
		# Create the form
		self.Name = "Create Window"
		self.Text = title
		self.Size = Size(500, 150)
		self.CenterToScreen()
		
		self.value = ""
		
		# Create label for number of divisions
		labelDiv = Label(Text = "Name of " + author + ":")
		labelDiv.Parent = self
		labelDiv.Size = Size(200, 150)
		labelDiv.Location = Point(30, 20)
		
		# Create TextBox for number of divisions
		self.textboxDiv = TextBox()
		self.textboxDiv.Parent = self
		self.textboxDiv.Text = "10"
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
				labelDiv = Label(Text = "Enter number please: ")

# Call the CreateWindow class and create the input for Drawer
formDrawer = CreateWindow("Change Parameter Drawn By", "Drawer")
Application.Run(formDrawer)

# Assign the input to variable
nameDrawer = formDrawer.value

# Call the CreateWindow class and create the input for Checker
formChecker = CreateWindow("Change Parameter Checked By", "Checker")
Application.Run(formChecker)

# Assign the input to variable
nameChecker = formChecker.value

# Store current document to variable
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Collects all sheets in current document
sheetsCollector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets) \
                                                .WhereElementIsNotElementType() \
                                                .ToElements()

# Create a Transaction group to group all subsequent transactions
tg = TransactionGroup(doc, "Update Drawn By and Checked By")

# Start the group transaction
tg.Start()

# Create a individual transaction to change the parameters on sheet
t = Transaction(doc, "Change Sheets Name")

# Start individual transaction
t.Start()

# Variable to store modified sheets
modSheets = list()

# Define function to modify parameter
def modParameter(param, checkEmpty, inputParam):
    # Store the sheet number parameter in variable
    sheetNumber = sheet.LookupParameter("Sheet Number").AsString()
    # Retrieve sheet parameter
    sheetDrawn = sheet.LookupParameter(param)
    # Convert parameter to string, check if it is empty and set it with user input
    if sheetDrawn.AsString() == checkEmpty:
        sheetDrawn.Set(inputParam)
        # Check if the sheet has been previously modified and append to list
        if sheetNumber not in modSheets:
            modSheets.append(sheetNumber)

# Loop through all sheets
for sheet in sheetsCollector:
    # Run function to modify Drawer
    modParameter("Drawn By", "Author", nameDrawer)
    # Call function to modify Checker
    modParameter("Checked By", "Checker", nameChecker)

# Print all changed sheets
print(modSheets)

# Commit individual transaction
t.Commit()

# Combine all individual transaction in the group transaction
tg.Assimilate()
