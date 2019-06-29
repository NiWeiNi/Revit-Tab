# -*- coding: utf-8 -*-
"""Isolates selected categories and overriden the rest of them with 90% transparency.
"""
__title__ = 'Isolate\nCategory'
__author__ = "nWn"

# Import commom language runtime
import clr

# Import Revit DB
from Autodesk.Revit.DB import OverrideGraphicSettings, Transaction, TransactionGroup

# Import libraries to enable Windows forms
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
"""
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
"""
# Store current document to variable
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Retrieve current view
activeView = doc.ActiveView

# Retrieve all categories in the document
docCat = doc.Settings.Categories

# Override tranparency settings
overtransparency = OverrideGraphicSettings()
overtransparency.SetSurfaceTransparency(50)

# Create a individual transaction
t = Transaction(doc, "Override category visibility")
# Start individual transaction
t.Start()

# Override all categories transparency
for c in docCat:
	try:
		activeView.SetCategoryOverrides(c.Id, overtransparency)
	except:
		pass

# Commit transaction
t.Commit()