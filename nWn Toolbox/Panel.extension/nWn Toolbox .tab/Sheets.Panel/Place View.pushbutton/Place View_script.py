# -*- coding: utf-8 -*-
"""Fills in empty Drawn by and Checked by parameters with custom input.

NOTE: 
Already filled in parameters will not be overridden."""
__title__ = 'Fill in\nDrawn'
__author__ = "nWn"

# Import commom language runtime
import clr

# Import Revit DB
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, \
                            Transaction, TransactionGroup

# Import libraries to enable Windows forms
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

from System.Drawing import Point, Size
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

# Store current document to variable
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Collects all sheets in current document
sheetsCollector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets) \
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
    # Check if it is by default and input is not empty, set it with user input
    if sheetDrawn.AsString() == checkEmpty and inputParam != "":
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

# Commit individual transaction
t.Commit()

# Combine all individual transaction in the group transaction
tg.Assimilate()

# Print all changed sheets
print("The following sheets have been modified: \n\n" + "\n".join(modSheets))