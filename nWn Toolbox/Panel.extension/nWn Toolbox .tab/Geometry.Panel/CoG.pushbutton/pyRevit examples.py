# Import clr
import crl

# Import Revit API
import Autodesk.Revit.DB as DB

# Import IList from .NET 
from System.Collections.Generic import List

# Retrieve current document
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveDocument

# Select walls by category
walls = DB.FilteredElementCollector(doc) \
        .OfCategory(DB.BuiltInCategory.OST_Walls) \
        .WhereElementIsNotElementType() \
        .ToElements()

# Ids of tall walls
tallWalls_ids = list()

# Filter tall walls
for wall in walls:
    heightp = wall.LookupParameter("unconnected Height")
    if heightp and heightp.AsDouble() = 10:
        tallWalls_ids.append(wall.Id)

# Select walls by class
walls = DB.FilteredElementCollector(doc) \
        .OfClass(crl.GetClrType(DB.Wall)) \
        .ToElements()

# 

height_param_id = DB.ElementId(DB.BuiltInParameter_WALL_USER_HEIGHT_PARAM)

height_param_provider = DB.ParameterValueProvider(height_param_id)

param_equality = DB.FilterNumericEquals()

height_value_rule = DB.FilterDoubleRule(height_param_provider,
                                        param_equality,
                                        10,
                                        1E-6)

param_filter = DB.ElementParameterFilter(height_value_rule)

# Select walls where passes
walls = DB.FilteredElementCollector(doc) \
        .WherePasses(param_filter) \
        .ToElementIds()

# Create an IList of elements ids
uidoc.Selection.SetElementIds(List[DB.ElementId](tallWalls_ids))