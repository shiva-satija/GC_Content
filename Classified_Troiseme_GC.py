'''
Created:	E. Reichenberger
Date:	3.8.2013

Purpose: To merge classified sequences file to original fasta file into one while calculating the GC% from the 1st, 2nd, and 3rd position for sequences as well as the overal gc content. Data is saved as fasta file.

Addendum 4.24.2013: Add ability to add filename to end of python call: python test.py arg1 arg2 arg3
and call the script from a bash script.
'''

import Bio
import os
import glob
import sys
import re #regular expressions
import inspect
import collections
from Bio.SeqUtils import GC123
from Bio.SeqUtils import GC

########################FILE INFORMATION###############################

arguments = sys.argv
#print arguments
#['/data/erin/Ruti/TroisiemeCodon_Position/Classified_Troiseme_GC.py', 'Diamond_fork_biofilm_4460448.fa', '/home/erin/Ruti/TroisiemeCodon_Position/ENVIRONMENTS/Water/Fresh/Stream/Diamond_fork_biofilm_4460448/Phylum/results.03.phymmBL__Diamond_fork_biofilm_4460448_fa.txt', 'classified_GC_Diamond_fork_biofilm_4460448.fa']

fastaSequenceFileName = arguments[1] #This is the original fasta (unsplit) file
fastaSequenceFileName = fastaSequenceFileName.replace(' ', '')
resultsPhymmBL_fileName = arguments[2] #This is the results_03_PhymmBL... file
resultsPhymmBL_fileName = resultsPhymmBL_fileName.replace(' ', '')
classifiedFileName = arguments[3] #This is the name of the output file

results_content = open(resultsPhymmBL_fileName, 'r')
results_lines = []
resultsFiles = results_content.readlines()

for results in resultsFiles:
	results_lines.append(results)

results_content.close()

########################Removing Old Files###############################
if os.path.exists(classifiedFileName):
	os.remove(classifiedFileName)
outputFile = open(classifiedFileName, 'a')

outputFile.write('#QUERY_ID' + '\t' + 'BEST_MATCH' + '\t' + 'SCORE' + '\t' + 'GENUS' + '\t' + 'GENUS_CONF' + '\t' + 'FAMILY' + '\t' + 'FAMILY_CONF' + '\t' + 'ORDER' + '\t' + 'ORDER_CON' + '\t' + 'CLASS' + '\t' + 'CLASS_CONF' + '\t' + 'PHYLUM' + '\t' + 'PHYLUM_CONF' + '\t' + 'GC_1' + '\t' + 'GC_2' + '\t' + 'GC_3' + '\t' + 'GC_overall' + '\n')

inputFasta_fileLines = open(fastaSequenceFileName, 'r')
Fasta_fileLines = inputFasta_fileLines.readlines()
fastaArray = []
resultsArray = []
count = 1
for i in range(0, len(Fasta_fileLines) - 1):
	lines = Fasta_fileLines[i]
	if lines.startswith('>'):
		id_Fasta = lines.strip('>')
		id_Fasta = id_Fasta.strip('\n')
		Strings = str(results_lines[count])
		fastaArray.append(Strings)
		results_lines[count] = results_lines[count].strip('\n')

	if Strings.startswith(id_Fasta):
		resultsArray.append(Strings)
		gc_1 = round(GC123(Fasta_fileLines[i+1])[1], 2)
		gc_2 = round(GC123(Fasta_fileLines[i+1])[2], 2)
		gc_3 = round(GC123(Fasta_fileLines[i+1])[3], 2)
		gc_overall = round(GC(Fasta_fileLines[i+1]), 2)
		outputFile.write('>' + results_lines[count] + '\t' + str(gc_1) + '\t' + str(gc_2) + '\t' + str(gc_3) + '\t' + str(gc_overall) + '\n')
		outputFile.write(Fasta_fileLines[i+1])
		count+=1

print len(fastaArray)
print len(resultsArray)

inputFasta_fileLines.close()
outputFile.close()
