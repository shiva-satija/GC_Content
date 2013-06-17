'''
Author:  E. Reichenberger
Date:    6.4.2013

Purpose: Move specific text files from the PhymmBL to the current working directory. The moved files will be related to the files in the working directory. 
     This is important if the scoreReads.pl script is run on more than one file (with different working directories) at a time. Moving all text files
     in the PhymmBL without discrimination would potentially move some text files to the wrong directory.

Call file like so:
python $scriptPathway/moveResultFiles.py $PWD $PhymmBL_directory $Environment_Directory $errFile $rawBlastOutput $rawPhymmOutput $results1 $results2 $results3 $tempRev $fileName_noExt

For example:
This script will be called from a bash script where the arguments will be defined within the bash script.

Below are the potential types of files
errFile__home_...fileName_noExt
rawBlastOutput__home_...fileName_noExt
rawPhymmOutput__home_...fileName_noExt
results.01.phymm__home_...fileName_noExt
results.02.blast__home_...fileName_noExt
results.03.phymmBL__home_...fileName_noExt
tempRev__home_...fileName_noExt
tempRev__home_...fileName_noExt

'''

import os
import glob
import sys
import re #regular expressions
import shutil

arguments = sys.argv
workingDirectory = arguments[1] #$PWD will be the current working directory
workingDirectory = workingDirectory.replace('data', 'home') #PWD uses 'home' rather than 'data'
scoreRead_prefix = workingDirectory.replace('/', '_')
scoreRead_prefix = scoreRead_prefix.replace('.', '_')

path = arguments[2] #$PhymmBL_directory where (where results from the classifier are created)
environmentDirectory = arguments[1]
environmentDirectory_prefix = environmentDirectory.replace('/', '_')
fileName_noExt=arguments[10]
fileName_noExt = fileName_noExt.replace('.', '_')

for i in range(len(arguments)):
	if i > 2 and i < 10:
		arguments[i] = path + '/' +  arguments[i] + '_' + scoreRead_prefix + '_' + fileName_noExt

errFile = arguments[3]  
rawBlastOutput = arguments[4] 
rawPhymmOutput = arguments[5]
results1 = arguments[6]
results2 = arguments[7]
results3 = arguments[8]
tempRev = arguments[9]

infiles = []
outfiles = []

for infile in glob.glob(os.path.join(path, '*.txt') ): #file extension type
	infiles.append(infile)
	if infile.startswith(errFile) or infile.startswith(rawBlastOutput) or infile.startswith(rawPhymmOutput) or infile.startswith(results1) or infile.startswith(results2) or infile.startswith(results3) or infile.startswith(tempRev):
		#newfile = infile.replace(environmentDirectory_prefix, '')
		newfile = infile.replace(path, '')
		#newfile = newfile.replace(scoreRead_prefix, '')
		#outfiles.append(newfile)
		#print newfile
		os.rename(infile, 'output/'+ newfile)
