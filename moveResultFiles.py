'''
Author:  E. Reichenberger
Date:    6.4.2013

Purpose: Move specific text files from the PhymmBL to the current working directory. The moved files will be related to the files in the working directory. 
     This is important if the scoreReads.pl script is run on more than one file (with different working directories) at a time. Moving all text files
     in the PhymmBL without discrimination would potentially move some text files to the wrong directory.

Call file like so:
python moveResultFiles.py $PWD $PhymmBL_directory $Environment_directory

For example:
00
PWD = "/data/erin/Ruti/TroisiemeCodon_Position/ENVIRONMENTS/Soil/Prairie/4502935.3"
PhymmBL_directory="/data/erin/Ruti/TroisiemeCodon_Position/PhymmBL"
Environment_directory="/data/erin/Ruti/TroisiemeCodon_Position/ENVIRONMENTS/"         
This script will be called from a bash script where the arguments will be defined within the bash script.

Below are the potential types of files
errFile__home_erin_Ruti_TroisiemeCodon_Position_ENVIRONMENTS_Soil_Desert_4EB024_r1_4477904_3_Phylum_4EB024_r1_4477904_3_59_fa.txt
rawBlastOutput__home_erin_Ruti_TroisiemeCodon_Position_ENVIRONMENTS_Soil_Desert_4EB024_r1_4477904_3_Phylum_4EB024_r1_4477904_3_00_fa.txt
rawPhymmOutput__home_erin_Ruti_TroisiemeCodon_Position_ENVIRONMENTS_Soil_Desert_4EB024_r1_4477904_3_Phylum_4EB024_r1_4477904_3_63_fa.txt
results.01.phymm__home_erin_Ruti_TroisiemeCodon_Position_ENVIRONMENTS_Soil_Desert_4EB024_r1_4477904_3_Phylum_4EB024_r1_4477904_3_00_fa.txt
results.02.blast__home_erin_Ruti_TroisiemeCodon_Position_ENVIRONMENTS_Soil_Desert_4EB024_r1_4477904_3_Phylum_4EB024_r1_4477904_3_00_fa.txt
results.03.phymmBL__home_erin_Ruti_TroisiemeCodon_Position_ENVIRONMENTS_Soil_Desert_4EB024_r1_4477904_3_Phylum_4EB024_r1_4477904_3_03_fa.txt
tempRev__home_erin_Ruti_TroisiemeCodon_Position_ENVIRONMENTS_Soil_Desert_4EB024_r1_4477904_3_Phylum_4EB024_r1_4477904_3_59_fa.txt

'''

import os
import glob
import sys
import re #regular expressions
import shutil
#python $scriptPathway/moveResultsFiles.py $PWD $PhymmBL_directory $Environment_Directory $errFile $rawBlastOutput $rawPhymmOutput $results1 $results2 $results3 $tempRev 

arguments = sys.argv
print arguments
workingDirectory = arguments[1] #$PWD will be the current working directory
workingDirectory = workingDirectory.replace('data', 'home') #PWD uses 'home' rather than 'data'
#workingDirectory = workingDirectory.replace('home', 'data') #PWD uses 'home' rather than 'data'
scoreRead_prefix = workingDirectory.replace('/', '_')

path = arguments[2] #$PhymmBL_directory where (where results from the classifier are created)
environmentDirectory = arguments[3]
environmentDirectory_prefix = environmentDirectory.replace('/', '_')

errFile = arguments[4]
rawBlastOutput = arguments[5]
rawPhymmOutput = arguments[6]
results1 = arguments[7]
results2 = arguments[8]
results3 = arguments[9]
tempRev = arguments[10]

infiles = []
outfiles = []

for infile in glob.glob(os.path.join(path, '*.txt') ): #file extension type
     infiles.append(infile)
     if scoreRead_prefix in infile:   #Alternative: if not tempString in files:
          newfile = infile.replace(path, '')
          newfile = newfile.replace('/', '')
          newfile = newfile.replace(scoreRead_prefix, '')
          newfile = newfile.replace(environmentDirectory_prefix, '')
          outfiles.append(newfile)
          os.rename(infile, 'output/'+ newfile)
