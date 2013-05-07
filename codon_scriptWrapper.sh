#!/bin/bash

#-------------------------------------------------------------------#
function splitFiles {

# splitFiles will 
#1. Accept a user input file (e.g. fileName)
#2. Split the file into 6 parts where the number of lines in each part is equally divisible by 2. 
#3. Rename the files as fileName_1, fileName_2....

echo "Enter the name of the fasta file to split into 6 parts (followed by [ENTER]):"
read fileName

#echo $fileName
export fileName
fileName_noExt=${fileName:0:-3}
#echo $fileName_noExt
export fileName_noExt

LineNumber=$(wc -l < "$fileName")
#echo "LineNumber = $LineNumber"

counter=0
let Remainder=LineNumber/6
let Modulus_six=LineNumber%6
let Modulus_two=Remainder%2

if [ $Modulus_six -eq 0 ] && [ $Modulus_two -eq 0 ]
then
	split -l $Remainder $fileName $fileName_noExt'_'
fi

if [ $((LineNumber%6)) -ne 0 ] || [[ $((LineNumber%6)) -eq 0 && $((Modulus_two)) -ne 0 ]]
then
	let counter+=1
	until [ $((LineNumber%6)) -eq 0 ] && [ $(((LineNumber/6)%2)) -eq 0 ]; do
		let counter=counter
		let LineNumber=LineNumber+counter
	done
	
	let Remainder=LineNumber/6
	split -l $Remainder $fileName $fileName_noExt'_'
fi

#echo "LineNumber = $LineNumber"
mv $fileName_noExt'_aa' $fileName_noExt'_1.fa'
mv $fileName_noExt'_ab' $fileName_noExt'_2.fa'
mv $fileName_noExt'_ac' $fileName_noExt'_3.fa'
mv $fileName_noExt'_ad' $fileName_noExt'_4.fa'
mv $fileName_noExt'_ae' $fileName_noExt'_5.fa'
mv $fileName_noExt'_af' $fileName_noExt'_6.fa'

len=$(wc -l < $fileName)
len1=$(wc -l < $fileName_noExt'_1.fa')
len2=$(wc -l < $fileName_noExt'_2.fa')
len3=$(wc -l < $fileName_noExt'_3.fa')
len4=$(wc -l < $fileName_noExt'_4.fa')
len5=$(wc -l < $fileName_noExt'_5.fa')
len6=$(wc -l < $fileName_noExt'_6.fa')
lenSplit=$((len1 + $len2 + $len3 + $len4 + $len5 + $len6))

#wc -l $fileName_noExt'_1.fa'
#wc -l $fileName_noExt'_2.fa'
#wc -l $fileName_noExt'_3.fa'
#wc -l $fileName_noExt'_4.fa'
#wc -l $fileName_noExt'_5.fa'
#wc -l $fileName_noExt'_6.fa'
#wc -l $fileName

if [ $lenSplit -ne $len ]
#if [ $lenSplit -eq $len ]
then
  #echo "The total number of lines in the split file are equal to the number of lines in the orginal file. :)"
#else
  echo "There is a problem with the number of lines in the split files. Try again. :("
  exit
fi
#ls -lah
}
#-------------------------------------------------------------------#


#-------------------------------------------------------------------#
function scoreReads {
echo "Do you want to classify the reads? (Y/N followed by [ENTER]:"
read scoreRead_Response 

if [ $scoreRead_Response -eq "y" ] || [ $scoreRead_Response -eq "Y" ] || [ $scoreRead_Response -eq "yes" ] || [ $scoreRead_Response -eq "Yes" ] 
then
  cd /data/erin/Ruti/TroisiemeCodon_Position/PhymmBL/ 
  parallel ./scoreReads.pl ::: $dirpath/$fileName_noExt'_1.fa' $dirpath/$fileName_noExt'_2.fa' $dirpath/$fileName_noExt'_3.fa' $dirpath/$fileName_noExt'_4.fa' $dirpath/$fileName_noExt'_5.fa' $dirpath/$fileName_noExt'_6.fa' 
  cd -
fi
}
#-------------------------------------------------------------------#


#-------------------------------------------------------------------#
function makeDirectory {
#If an output directory does not exist in working directory, make it.
DIRECTORY=output
if [ ! -d "$DIRECTORY" ]; then
	mkdir $DIRECTORY 
fi
}
#-------------------------------------------------------------------#


#-------------------------------------------------------------------#
function moveFiles {
declare -a resultFiles=(`ls /home/erin/Ruti/TroisiemeCodon_Position/PhymmBL/results.03.phymmBL*.txt`) 
cp ${resultFiles[@]} .  
lengthB=$(expr length ${resultFiles[1]})
lengthA=$(expr length "/home/erin/Ruti/TroisiemeCodon_Position/PhymmBL/")
fileName2=${resultFiles[1]:lengthA:lengthB}
export fileName2
lengthF=$(expr length $dirpath)
partial_dir=${dirpath:40:$lengthF} #results.03.phymmBL__home_erin_Ruti_TroisiemeCodon_Position_
partial_dir=${partial_dir:0:-7} # = Wegley/Porites_Astreoides/Phylum
partial_dir=`echo ${partial_dir} | tr "/" _` # = Wegley/Porites_Astreoides/Phylum
export partial_dir
#echo $partial_dir #echo ${partial_dir:0:-7} | tr "/" _ # = Wegley/Porites_Astreoides/Phylum
cp /home/erin/Ruti/TroisiemeCodon_Position/PhymmBL/*.txt output/. #Move all txt files from PhymmBL to output directory (in working directory)
}
#-------------------------------------------------------------------#


#-------------------------------------------------------------------#
function catFiles {
# This function will 
#1. Accept a user input file (e.g. results.03.phymmBL____Dinsdale_Line_Islands_Christmas_Reef_PhymmBL_4440041_3_XmasLIMic080505_5_fa.txt)
#2. Cat all the results files together 
#	i. Keep initial line but remove dups of QUERY_ID       BEST_MATCH      SCORE   GENUS   GENUS_CONF      FAMILY  FAMILY_CONF     ORDER   ORDER_CON       CLASS   CLASS_CONF      PHYLUM  PHYLUM_CONF     GC_1    GC_2    GC_3    GC_overall

base_fileName=${fileName2:0:-9}
export basefileName
cat $base_fileName'_1_fa.txt' <(sed 1d $base_fileName'_2_fa.txt') <(sed 1d $base_fileName'_3_fa.txt') <(sed 1d $base_fileName'_4_fa.txt') <(sed 1d $base_fileName'_5_fa.txt') <(sed 1d $base_fileName'_6_fa.txt') > $base_fileName'_fa.txt'
}
#-------------------------------------------------------------------#


#-------------------------------------------------------------------#
function Classified_Troiseme_GC {
#Purpose: To merge classified sequences file to original fasta file into one while calculating the GC% from the 1st, 2nd, and 3rd position for sequences as well as the overal gc content. Data is saved as fasta file.

#Steps:
#1. Create text file (write mode)
#2. Loop through directory to make list of all pertinant files 
#3. Loop through all *.gb files
#        i. Open GenBank files (read mode)
#        ii. extract pertinent info from each SEQ record
#                a. Use taxID to generate taxonomic assignment (separate module) avoids naming inconsistency found in genbank files
#        iii. concatenate info to end of txt file (tab delimated form)
#        iv. concatenate sequence of SEQ record to end of text fi

python /data/erin/Ruti/TroisiemeCodon_Position/Classified_Troiseme_GC.py $fileName $base_fileName'_fa.txt'
}
#-------------------------------------------------------------------#


#-------------------------------------------------------------------#
function checkFileLength {
#verify # of lines in classified_GC.. file is 1 (ONE) greater than
#original unsplit fasta file

outputLen=`wc -l < $outputFileName`
inputLen=`wc -l < $fileName`
inputLen=$((inputLen+1))

if [ $outputLen -ne $inputLen ]
then
		echo "The number of lines in the classified file do not agree with the number of lines in orginal fasta file"
		echo "This program is terminating. Check the split files, check the classified file, and check the original file"
		exit
fi
}
#-------------------------------------------------------------------#


#-------------------------------------------------------------------#
function awkCommand {
#Purpose: takes classified file & extracts lines containing 17 columns (not all things get classified at each level)
# & copies the phylum name and the GC into pipeline which is sorted and copied into sorted file. 
completeClassifiedFilePath=$dirPath$outputFileName
sortedPhylumFile="phylum_sorted_"$partial_dir".txt"
export sortedPhylumFile
#echo $sortedPhylumFile

#command below assumes that the phylum will always be classified. #NF is the number of fields
awk '$1 ~ /^>/  && $(NF - 4) >= 0.8 {print $(NF - 5), $(NF - 4), $(NF - 3), $(NF - 2), $(NF - 1), $NF}' $completeClassifiedFilePath | sort > $sortedPhylumFile 
#command below works only when bacteria is classified at each level (phylum-genus)
#awk '$1 ~ /^>/  && NF == 17 {print $(NF - 5), $(NF - 4), $(NF - 3), $(NF - 2), $(NF - 1), $NF}' $completeClassifiedFilePath | sort > $sortedPhylumFile 
#awk '$1 ~ /^>/  && NF != 17 {print $1, $(NF - 5), $(NF - 4), $(NF - 3), $(NF - 2), $(NF - 1), $NF, $0}' $completeClassifiedFilePath #checking for line !=17 
awk '$1 ~ /^[A-Z]/  {print $0}' $sortedPhylumFile > tempFile.txt #This will copy lines that start with a letter into tempFile
mv tempFile.txt $sortedPhylumFile
cp $sortedPhylumFile /data/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/. 
}
#-------------------------------------------------------------------#


#-------------------------------------------------------------------#
function uniquePhyla {
#Purpose: go through sorted file for unique phyla names, append to
#"unique_phyla.txt" (in Sorted_Phylum directory)
# go through text file to ensure unique names exist only

awk '{ print $1}' $sortedPhylumFile | uniq > unique_phyla.txt
cat unique_phyla.txt /data/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/unique_phyla.txt >> /data/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/temp_unique_phyla.txt
#cp  /data/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/unique_phyla.txt  /data/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/temp_file.txt
sort /data/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/temp_unique_phyla.txt > /data/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/sort_temp_unique_phyla.txt
uniq /data/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/sort_temp_unique_phyla.txt > /data/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/unique_phyla.txt
rm  /data/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/sort_temp_unique_phyla.txt 
rm  /data/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/temp_unique_phyla.txt 
}
#-------------------------------------------------------------------#


#-------------------------------------------------------------------#
function comparePhyla {
# Given: 
# Acidobacteria 0.711 55.56 41.18 70.59 54.72
# Acidobacteria 0.809 52.17 73.91 63.64 62.32
# Acidobacteria 0.833 51.72 71.43 50.0 56.98
# Acidobacteria 0.834 68.97 57.14 57.14 60.47
# Acidobacteria 0.836 45.71 62.86 45.71 50.94
# Acidobacteria 0.837 51.52 54.55 60.61 55.0

# Purpose: Get phylum name, #of idential phylum names, the max, min, and average for the confidence, GC_1, GC_2, GC_3, and GC_overall.
# This creates a comparison file of all phyla. Input is a unique_phyla.txt file.
python /data/erin/Ruti/TroisiemeCodon_Position/compare_phyla.py
}
#-------------------------------------------------------------------#

#_-----------------FUNCTION CALLS-----------------------------------#
SERVICE="scoreReads.pl"
RESULT=`ps -A | sed -n /${SERVICE}/p`
splitFiles #call splitFiles function
dirpath=$PWD #copy name of working directory (containing split fasta files)
scoreReads
makeDirectory
moveFiles #114
catFiles #138
Classified_Troiseme_GC #154
outputFileName='classified_GC_'$fileName #get name of classified file
checkFileLength #172
awkCommand #191
uniquePhyla #212
comparePhyla
cp phyla_comparison.sh /home/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/.
rm /home/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/merged_phyla.txt
sh /home/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/phyla_comparison.sh
#-------------------------------------------------------------------#

exit $?
