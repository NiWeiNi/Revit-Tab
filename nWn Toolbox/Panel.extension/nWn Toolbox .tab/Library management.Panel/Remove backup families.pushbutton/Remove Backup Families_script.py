# -*- coding: utf-8 -*-
"""Remove backup files from a directory.

Note:
Please be as specific as possible selecting the folder,
as this script will remove all backup files in subfolders."""
__title__ = 'Remove\nBackup\nFiles'
__author__ = "nWn"

# Import clr
import clr

# Import python modules
import os, re, shutil

# Import libraries to create a Windows form
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Windows.Forms import Application, Form, StatusBar, FolderBrowserDialog
from System.Windows.Forms import RadioButton, GroupBox, DialogResult, Button
from System.Drawing import Size, Point

# Function to create Windows folder browser
def windBrowser():
	# Create folder browser window 
	dialog = FolderBrowserDialog()
	# Record for user action and store selected path
	if (dialog.ShowDialog() == DialogResult.OK):
		return dialog.SelectedPath

# Call windBrowser to select folder with backup files and store path to var
directory = windBrowser()

# Class to input user choice
class IForm(Form):
	def __init__(self):
		self.Text = "Remove or Move"
		self.Size = Size(360, 240)
		self.value = ""

		# Set style to the selection to the group box displaying the options
		gb = GroupBox()
		gb.Text = "Remove files or Move to Another Location"
		gb.Size = Size(300, 100)
		gb.Location = Point(20, 20)
		gb.Parent = self

		# Remove radius button
		remove = RadioButton()
		remove.Text = "Remove"
		remove.Parent = gb
		remove.Location = Point(10, 30)
		remove.CheckedChanged += self.OnChanged

		# Move radius button
		backup = RadioButton()
		backup.Text = "Move to Folder"
		backup.Parent = gb
		backup.Size = Size(200, 20)
		backup.Location = Point(10, 60)
		backup.CheckedChanged += self.OnChanged

		# Create button
		button = Button()
		button.Parent = self
		button.Text = "Ok"
		button.Location = Point(130, 130)

		# Register event
		button.Click += self.ButtonClicked

		# Display the window form to show in the middle of the screen
		self.CenterToScreen()

	# Functions to retrieve users input
	def ButtonClicked(self, sender, event):
		self.Close()

	def OnChanged(self, sender, event):
		if sender.Checked:
			self.value = sender.Text

# Call for the options form
buttonForm = IForm()
Application.Run(buttonForm)

# Check to move files or delete them
delMov = buttonForm.value

# Check if user selected backup option and store path for backups to var
backupDir = ""
if delMov == "Move to Folder":
	backupDir = windBrowser()

# Function to clean the backup files
def directoryClean(directory, backupDir):
	# Empty list to store the filenames that have been removed or moved
	modFiles = list()
	# Collect all files in directory and subdirectories
	for folderName, subFolders, files in os.walk(directory):
		# Pattern to check against if file is a revit family or project backup
		matchBackups = re.compile(r'.*\.\d+.r(vt|fa)$')
		# Loop over the files
		for file in files:
			# Assign the matched files to a variable
			matched = matchBackups.search(file)
			# If the file is a match
			if matched:
				# Get the original filepath for the file
				filePath = os.path.join(folderName, file)
				# Change matched files permission to writable
				os.chmod(filePath, 436)
				# Case False: Move backup files
				if delMov != "Remove":
					# Get the destination filepath for the file (move will overwrite previous versions if full path is provided)
					backupPath = os.path.join(backupDir, file)
					# If files moved to a subfolder in the directory, ignore the file as it has been already moved
					if filePath != backupPath:
						# Move matched files
						shutil.move(filePath, backupPath)
						# Append modified elements to modFiles list
						modFiles.append(file)
				# Case True: Delete backup files
				else:
					# Delete matched files
					os.unlink(filePath)
					# Append modified elements to modFiles list
					modFiles.append(file)
	return modFiles

# Call the function to execute
cleanBackup = directoryClean(directory, backupDir)

# Function to display result to user
def printMessage(resultList, message, messageWarning):
	if len(resultList) != 0:
		print(message)
		print("\n".join(resultList))
	else:
		print(messageWarning)

# Print message
printMessage(cleanBackup, "The following files has been changed:", "No files has been moved or deleted.")