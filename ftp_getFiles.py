'''
Created:  E. Reichenberger
Date:     5.29.2013

Purpose: Create bash script file that downloads a ftp files and renames them 
'''

import os
import re
import sys
import glob

arguments = sys.argv

partial_wgetCall = arguments[7] + ' ' +  arguments[1]
fileName = arguments[2]
wgetFile = arguments[3]
folderFile = arguments[4] #This is a list of the subfolders (datasets) in the project directory
extension = arguments[5] #extension for files
processed = arguments[6]
  
inputFile = open(folderFile, 'r')
outputFile = open(wgetFile, 'w')

outputFile.write('#!/bin/bash\n\n')

folderLines= inputFile.readlines()

for lines in folderLines:
     lines = lines.replace('\n', '')
     outputFile.write(partial_wgetCall + lines + '/' + processed + fileName + '\n')
     outputFile.write('mv ' + fileName + ' ' + lines + extension + '\n')

inputFile.close()
outputFile.close()
