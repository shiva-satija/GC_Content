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

originalFastaFile = arguments[1] #This is the original fasta (unsplit) file
originalFastaFile = originalFastaFile.replace(' ', '')
PhymmBLresultsFile = arguments[2] #This is the results_03_PhymmBL... file
PhymmBLresultsFile = PhymmBLresultsFile.replace(' ', '')
mergedFile = arguments[3] #This will be the name of the output file

inputResults = open(PhymmBLresultsFile, 'r')
resultLines = inputResults.readlines() #readlines() reads in entire file at once.
resultArray = []
resultLineArray = []

for results in resultLines:
	if results.startswith('QUERY_ID') == False:
		results = results.replace('\n', '')
		resultLineArray.append(results)
		tempResults = results.split('\t',1)
		results = tempResults[0] #this excludes everything except the sequence id
		resultArray.append(results)

inputResults.close()

########################Removing Old Files###############################
if os.path.exists(mergedFile):
	os.remove(mergedFile)
outputFile = open(mergedFile, 'a')

outputFile.write('#QUERY_ID\tBEST_MATCH\tSCORE\tGENUS\tGENUS_CONF\tFAMILY\tFAMILY_CONF\tORDER\tORDER_CON\tCLASS\tCLASS_CONF\tPHYLUM\tPHYLUM_CONF\tGC_1\tGC_2\tGC_3\tGC_overall\n')

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

		count = resultArray.index(id_Fasta)
		fastaLines[i+1] = fastaLines[i+1].strip('\n')
		gc_1 = round(GC123(fastaLines[i+1])[1], 2)
		gc_2 = round(GC123(fastaLines[i+1])[2], 2)
		gc_3 = round(GC123(fastaLines[i+1])[3], 2)
		gc_overall = round(GC(fastaLines[i+1]), 2)
		outputFile.write('>' + resultLineArray[count] + '\t' + str(gc_1) + '\t' + str(gc_2) + '\t' + str(gc_3) + '\t' + str(gc_overall) + '\n')
		outputFile.write(fastaLines[i+1] + '\n')
		resultArray.pop(count)
		resultLineArray.pop(count)

outputFile.close()
