# -*- coding: utf-8 -*-
"""Add type to families or modify parameters in this type if it already exists"""
__title__ = 'Add Types\nto Families'
__author__ = "nWn"

# Import 
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms

# Store current document into variable
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Import Python modules
import os
import re
