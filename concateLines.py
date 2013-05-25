'''
Created:  E. Reichenberger
Date:     5.24.2013

Purpose:  Concatenate multiple lines of a single sequences into a single line
'''

import os
import re
import sys
import glob


arguments = sys.argv

inputFastaFile = arguments[1]
inputfastaFile = inputFastaFile.replace(' ', '')

inputFile = open(inputFastaFile, 'r')
outputFile = open('temp.fa', 'w')

fastalines = inputFile.readlines()

sequence = ''

for lines in fastalines:
     lines = lines.replace('\n', '')
     if lines.startswith('>'):
          if sequence != '':
               outputFile.write(sequence + '\n')
               sequence = ''
          flag = 0
          outputFile.write(lines + '\n')
          sequence = ''
     else: 
          flag = 1
          if flag == 1:
               sequence = sequence + lines

outputFile.write(sequence)
inputFile.close()
outputFile.close()

os.rename('temp.fa', inputFastaFile)
