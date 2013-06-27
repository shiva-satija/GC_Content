'''
Author:	E. Reichenberger
Date:	6.26.2013 (A die memoria JAR 9.28.2003 - 6.26.2003)

Purpose:
	Given a list of datasets, write an sh file that will download the accompanying metatdata files from MG-Rast

Commandline variables (called by bash script) are as follows*:
wget="wget"
wgetCall="http://metagenomics.anl.gov/metagenomics.cgi?page=DownloadMetagenome&action=download_md&filename=mgm"
wgetFile="wget_metaFiles.sh"
metaExtension=".metadata.txt"
fileExt=".txt"
Oh="-O"
folder="folder"
*Subject to change

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
folder = arguments[7]

inputFile = open(folder, 'r')
outputFile = open(wgetFile, 'w')

outputFile.write('#!/bin/bash\n\n')

folderLines= inputFile.readlines()

for lines in folderLines:
	lines = lines.replace('\n', '')
	if lines.startswith('folder') == False and lines.startswith('wgetFiles.sh') == False and lines.startswith('wget_metaFiles.sh') == False:
		outputFile.write(wget + ' "' + wgetCall + lines + metaExtension + '" ' + Oh + ' ' + lines + fileExt + '\n')

inputFile.close()
outputFile.close()
