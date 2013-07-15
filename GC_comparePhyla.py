'''
Created: E. Reichenberger (err29@drexl.edu)
Date: 4.6.2013

Given: 
Acidobacteria 0.711 55.56 41.18 70.59 54.72
.
.
Acidobacteria 0.837 51.52 54.55 60.61 55.0

Purpose: Get phylum name, #of idential phylum names, the max, min, and average for the confidence, GC_1, GC_2, GC_3, and GC_overall.

Steps:
1. Create array containing unique phylum numes
2. Get a list of files (phylum_sorted_*.txt) in directory
3. Create comparison file 

'''

import os
import glob
import sys
import re #regular expressions
import httplib
import collections

arguments = sys.argv
uniquePhyla = arguments[1] + '/unique_phyla.txt'
mergedPhyla = arguments[1] + '/merged_phyla.txt'
uniquePhylum = open(uniquePhyla, 'r')

phyla = []
lines = uniquePhylum.readlines()

for line in lines:
  line = line.replace('\n', '')
  phyla.append(line)

uniquePhylum.close()

#########################################################################
# Get list of files in directory 
#########################################################################
fileList = [] 
path = arguments[1]
for infile in glob.glob(os.path.join(path, 'phylum_sorted_*.txt') ): #file extension type
  infile = infile.replace(path, '')  #removes directory name from file name
  fileList.append(infile)

#if os.path.exists('phyla):
#        os.remove(outputFile)

outputFile = open('phyla_comparison.sh', 'w')
outputFile.write('#!/bin/bash\n\n')
count = 0

for files in fileList:
  newFile = files.replace('.txt', '')
  newFile = newFile.replace('phylum_sorted_', '')
  for phylum in phyla:
    if count == 0:
      #added $2>.79 5.1.2013
      #outputFile.write('awk \'$1 == \"' + phylum + '\" ' + '{rows++; sumConfidence +=$2; sumGC_1 +=$3; sumGC_2 +=$4; sumGC_3 +=$5; sumGC_overall +=$6;} END {print \"' + \
      outputFile.write('awk \'$1 == \"' + phylum + '\"  && $2 > .79 ' + '{rows++; sumConfidence +=$2; sumGC_1 +=$3; sumGC_2 +=$4; sumGC_3 +=$5; sumGC_overall +=$6;} BEGIN {OFS = "\t"} END {print \"' + \
      phylum + '\", rows, sumConfidence/rows, sumGC_1/rows, sumGC_2/rows, sumGC_3/rows, sumGC_overall/rows, "' + newFile + '"}\' ' +  path + '/'  + files + ' > ' +  mergedPhyla + '\n')
    if count != 0:
      outputFile.write('awk \'$1 == \"' + phylum + '\" && $2 > .79 ' + '{rows++; sumConfidence +=$2; sumGC_1 +=$3; sumGC_2 +=$4; sumGC_3 +=$5; sumGC_overall +=$6;} BEGIN {OFS = "\t"}  END {print \"' + \
      phylum + '\", rows, sumConfidence/rows, sumGC_1/rows, sumGC_2/rows, sumGC_3/rows, sumGC_overall/rows, "' + newFile + '"}\' ' +  path + '/'  + files + ' >> ' +  mergedPhyla + '\n')
  count+=2      

outputFile.close()
