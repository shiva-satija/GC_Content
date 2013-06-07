'''
Created:	E. Reichenberger
Date:	3.8.2013

Purpose: To merge classified sequences file to original fasta file into one while calculating the GC% from the 1st, 2nd, and 3rd position for sequences as well as the overal gc content. Data is saved as fasta file.

Addendum 4.24.2013: Add ability to add filename to end of python call: python test.py arg1 arg2 arg3
and call the script from a bash script.

Addendum: Somehow the order between the original fasta file and the results PhymmBL do not align. Re-writing script to account for this -- however, this will be much slower.
If it is possible to revert to the previous method, the "count" variable would need to be re-introduced (start value == 1, first line in PhymmBL results file is a header) and the 
increment count for each time '>' is found in the original fasta file.
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

originalFastaFile = arguments[1] #This is the original fasta (unsplit) file
originalFastaFile = originalFastaFile.replace(' ', '')
PhymmBLresultsFile = arguments[2] #This is the results_03_PhymmBL... file
PhymmBLresultsFile = PhymmBLresultsFile.replace(' ', '')
mergedFile = arguments[3] #This will be the name of the output file

inputResults = open(PhymmBLresultsFile, 'r')
resultLines = inputResults.readlines() #readlines() reads in entire file at once.
resultArray = []

for results in resultLines:
	tempResults = results.split('\t',1)
	results = tempResults[0]
	resultArray.append(results)

inputResults.close()

########################Removing Old Files###############################
if os.path.exists(mergedFile):
	os.remove(mergedFile)
outputFile = open(mergedFile, 'a')

outputFile.write('#QUERY_ID' + '\t' + 'BEST_MATCH' + '\t' + 'SCORE' + '\t' + 'GENUS' + '\t' + 'GENUS_CONF' + '\t' + 'FAMILY' + '\t' + 'FAMILY_CONF' + '\t' + 'ORDER' + '\t' + 'ORDER_CON' + '\t' + 'CLASS' + '\t' + 'CLASS_CONF' + '\t' + 'PHYLUM' + '\t' + 'PHYLUM_CONF' + '\t' + 'GC_1' + '\t' + 'GC_2' + '\t' + 'GC_3' + '\t' + 'GC_overall' + '\n')

inputFasta = open(originalFastaFile, 'r')
fastaLines = inputFasta.readlines() #readlines() reads in entire file at once.
fastaArray = []

id_Fasta = ''

for i in range(0, len(fastaLines) - 1): #from 0 to the number of lines in the file minus one
	lines = fastaLines[i]
	if lines.startswith('>'):
		id_Fasta = lines.strip('>') #strip removes leading and trailing characters
		id_Fasta = id_Fasta.strip('\n') #strip removes leading and trailing characters
		id_Fasta = id_Fasta.strip('\s') #strip removes leading and trailing characters
		
		#if resultLines[count].startswith(id_Fasta):
		count = resultArray.index(id_Fasta)
		fastaLines[i+1] = fastaLines[i+1].strip('\n')
		gc_1 = round(GC123(fastaLines[i+1])[1], 2)
		gc_2 = round(GC123(fastaLines[i+1])[2], 2)
		gc_3 = round(GC123(fastaLines[i+1])[3], 2)
		gc_overall = round(GC(fastaLines[i+1]), 2)
		outputFile.write('>' + resultLines[count].strip('\n')  + '\t' + str(gc_1) + '\t' + str(gc_2) + '\t' + str(gc_3) + '\t' + str(gc_overall) + '\n')

inputFasta.close()
outputFile.close()
