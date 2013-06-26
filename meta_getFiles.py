'''
Author:	E. Reichenberger
Date:	6.26.2013 (A die memoria)

Purpose:
	Given a list of datasets, download the accompanying metatdata files from MG-Rast
'''

import os
import sys
import re
import glob

arguments = sys.argv
wget = arguments[1]
wgetCall = arguments[2]
wgetFile = arguments[3]
metaExtension = arguments[4]
fileExt = arguments[5]
Oh = arguments[6]

iFile = raw_input("Enter file name: ")

inputFile = open(iFile, 'r')
outputFile = open(wgetFile, 'w')

outputFile.write('#!/bin/bash\n\n')

folderLines= inputFile.readlines()

for lines in folderLines:
	lines = lines.replace('\n', '')
	outputFile.write(wget + ' ' = wgetCall + lines + metaExtension + ' ' + Oh + lines + fileExt + '\n')

inputFile.close()
outputFile.close()
