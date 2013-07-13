'''
Author:  E. Reichenberger
Date:    7.13.2013

Purpose: Looking through the list of the metadata files, there should be an accompanying phylum_sorted_''.txt file. Use the list of metadata files, compare them to the 
phylum_sorted* files to see which one still need to be processed. 
'''

import os
import glob
import sys
import re #regular expressions
import shutil

arguments = sys.argv
path = arguments[1] #$PhymmBL_directory where (where results from the classifier are created)

metadata = []
for infile in glob.glob(os.path.join(path, '*.3.txt') ): #file extension type
		newfile2 = infile.replace(path, '')
		metadata.append(newfile2)

path = arguments[2]

phylum_sorted = []
for infile in glob.glob(os.path.join(path, 'phylum_sorted_*.txt') ): #file extension type
		newfile1 = infile.replace(path, '')
		newfile1 = newfile1.replace('phylum_sorted_', '')
		phylum_sorted.append(newfile1)

print len(metadata)

for meta in metadata:
	for phylum in phylum_sorted:
		if phylum == meta:
			metadata.pop(metadata.index(phylum))	

print len(metadata)
outputFile = open('remaining_processingList.sh', 'w')
outputFile.write('#!/bin/bash\n\n')
    
for meta in metadata:
	meta = meta.replace('.txt', '')
	outputFile.write('find -name ' + meta + '.fa\n')

outputFile.close()
