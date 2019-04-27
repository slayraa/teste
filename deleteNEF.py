# -*- coding: utf-8 -*-
"""
Created on Wed Sep 3 12:21

Delete NEF for which there is no corresponding JPEG

@author: rain
"""

import os
import collections

def deleteNEF(cwd):

	listFiles = []
	extToDelete = '.NEF'

	for f in os.listdir(cwd):
		if (f[-3:] != ".py") and (f[0] != "."):
			listFiles.append(f[:-4])
	
	counter = collections.Counter(listFiles)

	for k in counter.keys():
		if counter[k] == 1:
			fRemove = k+extToDelete
			os.remove(fRemove)
			print(fRemove + " was deleted")

def moveNEF(cwd):
	directory = 'nef'

	if not os.path.exists(directory):
		os.makedirs(directory)

	for f in os.listdir(cwd):
		if (f[-3:] == "NEF"):
			os.rename(os.path.join(cwd,f), os.path.join(cwd,directory,f))


def moveBackNEF(cwd):
	directory = 'nef'

	for f in os.listdir(os.path.join(cwd,directory)):
		os.rename(os.path.join(cwd,directory,f), os.path.join(cwd,f))

	os.rmdir(os.path.join(cwd,directory))


def printOptions():
	print("  1: Move all the NEF files to another directory called nef.")
	print("  2: Move back all the NEF files.")
	print("  3: Delete all NEF files that do not have a corresponding jpeg.")
	print("  0: Quit.")

#Program starts here!
choice = 1

while choice != 0:
	printOptions()
	cwd = os.getcwd()

	choice = int(input("Please enter your choice: "))

	if choice == 1:
		moveNEF(cwd)
	elif choice == 2:
		moveBackNEF(cwd)
	elif choice == 3:
		deleteNEF(cwd)
	else:
		print("Good photos! Bye :)")
		break
