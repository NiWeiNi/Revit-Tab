# -*- coding: utf-8 -*-
"""Select doors in rooms and fill in parameters.

NOTE: Leave parameters unfilled will delete previous filled parameters.
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
class MultiStringWindow(Form):
	def __init__(self, title):
		# Create the form
		self.Name = "Create Window"
		self.Text = title
		self.Size = Size(370, 590)
		self.CenterToScreen()
		
		self.value = ""
		self.value1 = ""
		self.value2 = ""
		self.value3 = ""
		self.value4 = ""
		self.value5 = ""
		self.value6 = ""
		self.value7 = ""
		self.value8 = ""
		self.finalValue = []
		
		# Create label for input title
		labelDiv = Label(Text = "Door Type")
		labelDiv.Parent = self
		labelDiv.Size = Size(150, 20)
		labelDiv.Location = Point(30, 40)
		# Create TextBox for input
		self.textboxDiv = TextBox()
		self.textboxDiv.Parent = self
		self.textboxDiv.Text = ""
		self.textboxDiv.Location = Point(200, 40)

		# Create label for input title
		labelDiv1 = Label(Text = "Door Frame Type")
		labelDiv1.Parent = self
		labelDiv1.Size = Size(150, 20)
		labelDiv1.Location = Point(30, 80)
		# Create TextBox for input
		self.textboxDiv1 = TextBox()
		self.textboxDiv1.Parent = self
		self.textboxDiv1.Text = ""
		self.textboxDiv1.Location = Point(200, 80)

		# Create label for input title
		labelDiv2 = Label(Text = "Door Frame Finish")
		labelDiv2.Parent = self
		labelDiv2.Size = Size(150, 20)
		labelDiv2.Location = Point(30, 120)
		# Create TextBox for input
		self.textboxDiv2 = TextBox()
		self.textboxDiv2.Parent = self
		self.textboxDiv2.Text = ""
		self.textboxDiv2.Location = Point(200, 120)

		# Create label for input title
		labelDiv3 = Label(Text = "Door Leaf Type")
		labelDiv3.Parent = self
		labelDiv3.Size = Size(150, 20)
		labelDiv3.Location = Point(30, 160)
		# Create TextBox for input
		self.textboxDiv3 = TextBox()
		self.textboxDiv3.Parent = self
		self.textboxDiv3.Text = ""
		self.textboxDiv3.Location = Point(200, 160)
		
		# Create label for input title
		labelDiv4 = Label(Text = "Meeting Styles")
		labelDiv4.Parent = self
		labelDiv4.Size = Size(150, 20)
		labelDiv4.Location = Point(30, 200)
		# Create TextBox for input
		self.textboxDiv4 = TextBox()
		self.textboxDiv4.Parent = self
		self.textboxDiv4.Text = ""
		self.textboxDiv4.Location = Point(200, 200)

		# Create label for input title
		labelDiv5 = Label(Text = "Door Leaf Material")
		labelDiv5.Parent = self
		labelDiv5.Size = Size(150, 20)
		labelDiv5.Location = Point(30, 240)
		# Create TextBox for input
		self.textboxDiv5 = TextBox()
		self.textboxDiv5.Parent = self
		self.textboxDiv5.Text = ""
		self.textboxDiv5.Location = Point(200, 240)

		# Create label for input title
		labelDiv6 = Label(Text = "Door Leaf Finish")
		labelDiv6.Parent = self
		labelDiv6.Size = Size(150, 20)
		labelDiv6.Location = Point(30, 280)
		# Create TextBox for input
		self.textboxDiv6 = TextBox()
		self.textboxDiv6.Parent = self
		self.textboxDiv6.Text = ""
		self.textboxDiv6.Location = Point(200, 280)

		# Create label for input title
		labelDiv7 = Label(Text = "Fire/Smoke")
		labelDiv7.Parent = self
		labelDiv7.Size = Size(150, 20)
		labelDiv7.Location = Point(30, 320)
		# Create TextBox for input
		self.textboxDiv7 = TextBox()
		self.textboxDiv7.Parent = self
		self.textboxDiv7.Text = ""
		self.textboxDiv7.Location = Point(200, 320)

		# Create label for input title
		labelDiv8 = Label(Text = "Door Security")
		labelDiv8.Parent = self
		labelDiv8.Size = Size(150, 20)
		labelDiv8.Location = Point(30, 360)
		# Create TextBox for input
		self.textboxDiv8 = TextBox()
		self.textboxDiv8.Parent = self
		self.textboxDiv8.Text = ""
		self.textboxDiv8.Location = Point(200, 360)

		# Create label for input title
		labelDiv9 = Label(Text = "Misc")
		labelDiv9.Parent = self
		labelDiv9.Size = Size(150, 20)
		labelDiv9.Location = Point(30, 400)
		# Create TextBox for input
		self.textboxDiv9 = TextBox()
		self.textboxDiv9.Parent = self
		self.textboxDiv9.Text = ""
		self.textboxDiv9.Location = Point(200, 400)

		# Create label for input title
		labelDiv10 = Label(Text = "Comments")
		labelDiv10.Parent = self
		labelDiv10.Size = Size(150, 20)
		labelDiv10.Location = Point(30, 440)
		# Create TextBox for input
		self.textboxDiv10 = TextBox()
		self.textboxDiv10.Parent = self
		self.textboxDiv10.Text = ""
		self.textboxDiv10.Location = Point(200, 440)
	
		# Create button
		button = Button()
		button.Parent = self
		button.Text = "Ok"
		button.Location = Point(200, 490)
		button.Size = Size(100, 20)
		
		# Register event
		button.Click += self.ButtonClicked
		
	def ButtonClicked(self, sender, args):
		if sender.Click:
			# Handle non numeric cases
			try:
				self.value = self.textboxDiv.Text
				self.value1 = self.textboxDiv1.Text
				self.value2 = self.textboxDiv2.Text
				self.value3 = self.textboxDiv3.Text
				self.value4 = self.textboxDiv4.Text
				self.value5 = self.textboxDiv5.Text
				self.value6 = self.textboxDiv6.Text
				self.value7 = self.textboxDiv7.Text
				self.value8 = self.textboxDiv8.Text
				self.value9 = self.textboxDiv9.Text
				self.value10 = self.textboxDiv10.Text
				self.finalValue = [self.value, self.value1, self.value2, self.value3, self.value4, self.value5, self.value6, self.value7, self.value8, self.value9, self.value10]
				self.Close()
			except:
				self.Close()

# Select all doors
doorsFilter = DB.ElementCategoryFilter(DB.BuiltInCategory.OST_Doors)
doorsCollector = DB.FilteredElementCollector(doc).WherePasses(doorsFilter).WhereElementIsNotElementType().ToElements()

# Create set of Room Name
roomNames = sorted(list(set([d.LookupParameter("Room Name").AsString() for d in doorsCollector])))

# Create form to select doors by Room Name
roomNameDoors = forms.SelectFromList.show(roomNames, "Select Rooms with Doors to Add Parameters", 600, 600, multiselect=True)

# Select doors to modify
modiDoors = [d for d in doorsCollector if d.LookupParameter("Room Name").AsString() in roomNameDoors]

# Call the CreateWindow class
formDoorType = MultiStringWindow("Door Parameters")
Application.Run(formDoorType)
# Assign the input to variable
dParams = formDoorType.finalValue

# Set parameters for doors
# Create a individual transaction to change the parameters
t = DB.Transaction(doc, "Set Door Parameters")
# Start individual transaction
t.Start()
for d in modiDoors:
	# Use overloads with a string as IronPython will throw an error by using same string
	d.LookupParameter("Door Type").Set.Overloads[str](dParams[0])
	d.LookupParameter("Door Frame Type").Set.Overloads[str](dParams[1])
	d.LookupParameter("Door Frame Finish").Set.Overloads[str](dParams[2])
	d.LookupParameter("Door Leaf Type").Set.Overloads[str](dParams[3])
	d.LookupParameter("Meeting Styles").Set.Overloads[str](dParams[4])
	d.LookupParameter("Door Leaf Material").Set.Overloads[str](dParams[5])
	d.LookupParameter("Door Leaf Finish").Set.Overloads[str](dParams[6])
	d.LookupParameter("Door-Fire/Smoke").Set.Overloads[str](dParams[7])
	d.LookupParameter("Door Security").Set.Overloads[str](dParams[8])
	d.LookupParameter("Door Miscelaneous").Set.Overloads[str](dParams[9])
	d.LookupParameter("Door Comments").Set.Overloads[str](dParams[10])

# Commit transaction
t.Commit()