# -*- coding: utf-8 -*-
"""Select doors in rooms and fill in parameters.

NOTE: 
"""
__author__ = "nWn"
__title__ = "Fill Doors\n Params"

# Import 
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Import commom language runtime
import clr

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
		self.textboxDiv.Text = ""
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

# Select all doors
doorsFilter = DB.ElementCategoryFilter(DB.BuiltInCategory.OST_Doors)
doorsCollector = DB.FilteredElementCollector(doc).WherePasses(doorsFilter).WhereElementIsNotElementType().ToElements()

# Create set of Room Name
roomNames = sorted(list(set([d.LookupParameter("Room Name").AsString() for d in doorsCollector])))

# Create form to select doors by Room Name
roomNameDoors = forms.SelectFromList.show(roomNames, "View Templates", 600, 300, multiselect=True)

# Select doors to modify
modiDoors = [d for d in doorsCollector if d.LookupParameter("Room Name").AsString() in roomNameDoors]

# Create form to input parameters
# Call the CreateWindow class
formDoorType = CreateWindow("Door Parameter", "Input Door Type: ")
Application.Run(formDoorType)
# Assign the input to variable
doorType = formDoorType.value

# Call the CreateWindow class
formLeafFinish = CreateWindow("Door Parameter", "Input Leaf Finish: ")
Application.Run(formLeafFinish)
# Assign the input to variable
leafFinish = formLeafFinish.value

# Call the CreateWindow class
formFrameType = CreateWindow("Door Parameter", "Input Frame Type: ")
Application.Run(formFrameType)
# Assign the input to variable
frameType = formFrameType.value

# Call the CreateWindow class
formframeFinish = CreateWindow("Door Parameter", "Input Frame Finish: ")
Application.Run(formframeFinish)
# Assign the input to variable
frameFinish = formframeFinish.value

# User Input Door Parameters
userDoorParams = [doorType, leafFinish, frameType, frameFinish]