'''
Created: E. Reichenberger (err29@drexl.edu)
Date: 4.6.2013

Given: 
Acidobacteria 0.711 55.56 41.18 70.59 54.72
Acidobacteria 0.809 52.17 73.91 63.64 62.32
Acidobacteria 0.833 51.72 71.43 50.0 56.98
Acidobacteria 0.834 68.97 57.14 57.14 60.47
Acidobacteria 0.836 45.71 62.86 45.71 50.94
Acidobacteria 0.837 51.52 54.55 60.61 55.0

Purpose: Get phylum name, #of idential phylum names, the max, min, and average for the confidence, GC_1, GC_2, GC_3, and GC_overall.

Phylum Categories:
Acidobacteria
Actinobacteria
Aquificae
Bacteroidetes
Caldiserica
Chlamydiae
Chlorobi
Chloroflexi
Chrysiogenetes
Crenarchaeota
Deferribacteres
Deinococcus-Thermus
Dictyoglomi
Elusimicrobia
Euryarchaeota
Fibrobacteres
Firmicutes
Fusobacteria
Gemmatimonadetes
Ignavibacteria
Nitrospirae
Planctomycetes
Proteobacteria
Spirochaetes
Synergistetes
Tenericutes
Thaumarchaeota
Thermodesulfobacteria
Thermotogae
Verrucomicrobia

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

uniquePhylum = open('/home/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/unique_phyla.txt', 'r')
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
path = '/home/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/'
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
      outputFile.write('awk \'$1 == \"' + phylum + '\"  && $2 > .79 ' + '{rows++; sumConfidence +=$2; sumGC_1 +=$3; sumGC_2 +=$4; sumGC_3 +=$5; sumGC_overall +=$6;} END {print \"' + \
      phylum + '\", rows, sumConfidence/rows, sumGC_1/rows, sumGC_2/rows, sumGC_3/rows, sumGC_overall/rows, "' + newFile + '"}\' /home/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/'  + files + ' >  /home/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/merged_phyla.txt\n')
    if count != 0:
      outputFile.write('awk \'$1 == \"' + phylum + '\" && $2 > .79 ' + '{rows++; sumConfidence +=$2; sumGC_1 +=$3; sumGC_2 +=$4; sumGC_3 +=$5; sumGC_overall +=$6;} END {print \"' + \
      phylum + '\", rows, sumConfidence/rows, sumGC_1/rows, sumGC_2/rows, sumGC_3/rows, sumGC_overall/rows, "' + newFile + '"}\' /home/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/'  + files + ' >>  /home/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/merged_phyla.txt\n')
  count+=2      

outputFile.close()
