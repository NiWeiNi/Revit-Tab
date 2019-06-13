# -*- coding: utf-8 -*-
"""Creates views with harcoded view templates for all assemblies of a specific type.

NOTE: The views are harcoded and must be changed per project basis."""
__title__ = 'Create\nViews'
__author__ = "nWn"
# Import commom language runtime
import clr

# from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import FilteredElementCollector, ElementCategoryFilter, \
							BuiltInCategory, IntersectionResultArray, Transaction, \
							TransactionGroup, Curve, FamilySymbol

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Import modules to create windows dialogues in Revit for user input
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.Windows.Forms import *
from System.Drawing import *

# Import math module
import math

# Create variables to store current document
doc = DocumentManager.Instance.CurrentDBDocument
uidoc=DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

# Pick model curve in Revit document to place elements
# Code based on john pierson´s isolated select model elements node
TaskDialog.Show("Isolated Selection", "Pick curve to follow path")

sel1 = uidoc.Selection
obt1 = Selection.ObjectType.Element

# Define class to filter elements of category to select 
class CustomISelectionFilter(Selection.ISelectionFilter):
	def __init__(self, nom_categorie):
		self.nom_categorie = nom_categorie
	def AllowElement(self, e):
		if e.Category.Name == self.nom_categorie:
			return True
		else:
			return False
	def AllowReference(self, ref, point):
		return True

el_ref = sel1.PickObject(obt1, CustomISelectionFilter("Lines"))
		
# Stores the selected modelcurve into curve, marks it as Revit owned element and extracts geometry
curve = doc.GetElement(el_ref.ElementId).ToDSType(True).Curve

# Create a class form
class CreateWindow(Form):
	def __init__(self):
		# Create the form
		self.Name = "Create Window"
		self.Text = "Input number of divisions"
		self.Size = Size(500, 150)
		self.CenterToScreen()
		
		self.values = 0
		
		# Create label for number of divisions
		labelDiv = Label(Text = "Number of elements to place: ")
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
				self.values = round(float(self.textboxDiv.Text))
				self.Close()
			except:
				labelDiv = Label(Text = "Enter number please: ")

# Call the CreateWindow class and create the input for number of divisions
form = CreateWindow()
Application.Run(form)

# Assign the inout to numberElements
numberElements = form.values

collector = FilteredElementCollector(doc).OfClass(FamilySymbol).ToElements()

class SelectFromList(Form):

    """
    form = SelectFromList(floor_types.keys())
    form.show()
    if form.DialogResult == DialogResult.OK:
        chosen_type_name = form.selected
    """

    def __init__(self):
        
	    """
	    form = SelectFromList(floor_types.keys())
	    form.show()
	    if form.DialogResult == DialogResult.OK:
	        chosen_type_name = form.selected
	    """

    def __init__(self, title, options):
        """
        Args:
            title (str): Title of Prompt
            options (dict): Name:Object
            **sort (bool): Sort Entries
        """


        self.selected = None
        options = sorted(options)

        #  Window Settings
        self.Text = 'Select View Type'
        self.MinimizeBox = False
        self.MaximizeBox = False
        self.BackgroundColor = Color.White
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.ShowIcon = False
        self.CenterToScreen()

        combobox = ComboBox()
        combobox.Width = 500
        combobox.Height = 300
        combobox.DataSource = options
        self.combobox = combobox

        button = Button()
        button.Text = 'Select'
        button.Location = Point(0,100)
        button.Width = combobox.Width
        button.Height = 50
        button.Click += self.button_click

        self.Width = combobox.Width + 16
        self.Height = 300

        self.Controls.Add(combobox)
        self.Controls.Add(button)

    def button_click(self, sender, event):
        self.selected = self.combobox.SelectedValue
        self.DialogResult = DialogResult.OK
        self.Close()

    def show(self):
        """ Show Dialog """
        self.ShowDialog()
        
comb = SelectFromList("Select family to place in points", collector)
comboBox = Application.Run(comb)

familyInstance = comb.selected

# Check start and end points of the curve
startPoint = curve.StartPoint
endPoint = curve.EndPoint

# Divide curve
dividedCurve = curve.PointsAtEqualSegmentLength(numberElements)
finalCurve = list()

# Check if the strings of startPoint and endPoint are the same
if str(startPoint) == str(endPoint):
	# Closed curve, it needs only to add the start point
	finalCurve.append(startPoint)
	for el in dividedCurve:
		finalCurve.append(el)
else:
	# Open curve, needs both start and end points
	finalCurve.append(startPoint)
	for el in dividedCurve:
		finalCurve.append(el)
	finalCurve.append(endPoint)

# Create a list with tangent vectors to the curve at the division points
tangVector = list()

for point in finalCurve:
	tangVector.append(curve.TangentAtParameter(curve.ParameterAtPoint(point)))
	
# Create a list with the angle between the tangent vector and the curve	in radians
angleRot = list()
vectorX = Vector.XAxis()
vectorZ = Vector.ZAxis()

for vec in tangVector:
	angleRot.append(-vec.AngleAboutAxis(vectorX, vectorZ) * math.pi/180)

# Open transaction to place all the family instances
TransactionManager.Instance.EnsureInTransaction(doc)

instances = list()
placePoint = []
i = 0

for point in finalCurve:

	vec = Line.ByStartPointDirectionLength(point, vectorZ, 1).ToRevitType()
	
	instance = doc.Create.NewFamilyInstance(point.ToXyz(), familyInstance, StructuralType.NonStructural)
	ElementTransformUtils.RotateElement(doc, instance.Id, vec, angleRot[i])
	i = i +1
	
	instances.append(instance.Id)
	placePoint.append(instance.GetFamilyPointPlacementReferences())

items = List[ElementId](instances)

try:
	group = doc.Create.NewGroup(items);
	group.GroupType.Name = IN[3]
except:
	group = list()
	
# End Transaction
TransactionManager.Instance.TransactionTaskDone()

# Assign your output to the OUT variable.
OUT = instances
