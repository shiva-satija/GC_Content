#!/bin/bash

#-------------------------------------------------------------------#
function splitFiles {

# splitFiles will 
#1. Accept a user input file (e.g. fileName)
#2. Split the file into 6 parts where the number of lines in each part is equally divisible by 2. 
#3. Rename the files as fileName_1, fileName_2....

#echo "Enter the name of the fasta file to split into 6 parts (followed by [ENTER]):"
#read fileName #e.g. 4502935.3.fa
fileName="test.fa"
echo $fileName
echo "How many processors do you want to use? (followed by [ENTER])?:"
read processors
export processors

export fileName
fileName_noExt=${fileName:0:-3} #e.g. 4502935.3
export fileName_noExt

LineNumber=$(wc -l < "$fileName")

divider=2
counter=0
let Remainder=$((LineNumber/processors))
let Modulus_processor=$((LineNumber%processors))
let Modulus_two=$((Remainder%divider))

if [ $Modulus_processor -eq 0 ] && [ $Modulus_two -eq 0 ]
then
     split -l $Remainder $fileName $fileName_noExt'_' -d --additional-suffix=.fa
fi

if [ $((LineNumber%processors)) -ne 0 ] || [[ $((LineNumber%processors)) -eq 0 && $((Modulus_two)) -ne 0 ]]
then
	let counter+=1
	until [ $((LineNumber%processors)) -eq 0 ] && [ $(((LineNumber/processors)%divider)) -eq 0 ]; do
		let counter=counter
		let LineNumber=LineNumber+counter
	done
	
	let Remainder=$((LineNumber/processors))
     split -l $Remainder $fileName $fileName_noExt'_' -d --additional-suffix=.fa
fi

#for i in $(eval echo {0..$processors})
#do
#   #echo $fileName_noExt'_'${numArray[i]}'.fa'
#   fileLength=$(wc -l $fileName_noExt'_'${numArray[i]}'.fa')
# done
}
#-------------------------------------------------------------------#


#-------------------------------------------------------------------#
function scoreReads {
echo "Do you want to classify the reads? (Y/N followed by [ENTER]:"
read scoreRead_Response 

if [ $scoreRead_Response = "y" ] || [ $scoreRead_Response = "Y" ] || [ $scoreRead_Response = "yes" ] || [ $scoreRead_Response = "Yes" ] 
then
  #python call_PhymmBL.py $processors $fileName_noExt 
  #cp call_PhymmBL.sh /data/erin/Ruti/TroisiemeCodon_Position/PhymmBL/.
  cd /data/erin/Ruti/TroisiemeCodon_Position/PhymmBL/ 
  seq -w 0 $(($processors-1)) | parallel ./scoreReads.pl $dirpath/$fileName_noExt'_'{}'.fa'
  #sh call_PhymmBL.sh 
  #parallel ./scoreReads.pl ::: $dirpath/$fileName_noExt'_1.fa' $dirpath/$fileName_noExt'_2.fa' $dirpath/$fileName_noExt'_3.fa' $dirpath/$fileName_noExt'_4.fa' $dirpath/$fileName_noExt'_5.fa' $dirpath/$fileName_noExt'_6.fa' 
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
#pretty ugly function. multiple if statement as if [ **"$TEXTfiles" != "0"** ] will fail if there are no files present
#but it will run properly if it is the first time running the script.

#if i need to re-run the script, if [ -e /home/erin/Ruti/TroisiemeCodon_Position/PhymmBL/results.03.phymmBL*.txt ] will 
#fail if there are more than 1 files present (-e takes 1 variable only). When re-running this script, the files
#will have been moved (hence the else statement

#having both if statements will guarantee an error, but one if command will run and the entire script will continue
#running if there is a error.

#if multiple result files exist
TEXTfiles=$(ls /home/erin/Ruti/TroisiemeCodon_Position/PhymmBL/results.03.phymmBL*.txt 2> /dev/null | wc -l)
if [ **"$TEXTfiles" != "0"** ]
then 
  declare -a resultFiles=(`ls /home/erin/Ruti/TroisiemeCodon_Position/PhymmBL/results.03.phymmBL*.txt`) 
  mv ${resultFiles[@]} .  
  lengthB=$(expr length ${resultFiles[1]})
  lengthA=$(expr length "/home/erin/Ruti/TroisiemeCodon_Position/PhymmBL/")
  fileName2=${resultFiles[1]:lengthA:lengthB}
  export fileName2
  lengthF=$(expr length $dirpath)
  partial_dir=${dirpath:40:$lengthF} #results.03.phymmBL__home_erin_Ruti_TroisiemeCodon_Position_
  partial_dir=${partial_dir:0:-7} # = Wegley/Porites_Astreoides/Phylum
  partial_dir=`echo ${partial_dir} | tr "/" _` # = Wegley/Porites_Astreoides/Phylum
  export partial_dir
fi

#if there are zero result text file
if [ -e /home/erin/Ruti/TroisiemeCodon_Position/PhymmBL/results.03.phymmBL*.txt ]
then 
  declare -a resultFiles=(`ls /home/erin/Ruti/TroisiemeCodon_Position/PhymmBL/results.03.phymmBL*.txt`) 
  mv ${resultFiles[@]} .  
  lengthB=$(expr length ${resultFiles[1]})
  lengthA=$(expr length "/home/erin/Ruti/TroisiemeCodon_Position/PhymmBL/")
  fileName2=${resultFiles[1]:lengthA:lengthB}
  export fileName2
  lengthF=$(expr length $dirpath)
  partial_dir=${dirpath:40:$lengthF} #results.03.phymmBL__home_erin_Ruti_TroisiemeCodon_Position_
  partial_dir=${partial_dir:0:-7} # = Wegley/Porites_Astreoides/Phylum
  partial_dir=`echo ${partial_dir} | tr "/" _` # = Wegley/Porites_Astreoides/Phylum
  export partial_dir
else
  declare -a resultFiles=(`ls results.03.phymmBL*.txt`) 
  fileName2=$resultFiles
  export fileName2
fi

TEXTfiles=$(ls /home/erin/Ruti/TroisiemeCodon_Position/PhymmBL/*.txt 2> /dev/null | wc -l)
if [ **"$TEXTfiles" != "0"** ]
then
  mv `/home/erin/Ruti/TroisiemeCodon_Position/PhymmBL/*.txt output/.` #Move all txt files from PhymmBL to output directory (in working directory)
fi

if [ -e /home/erin/Ruti/TroisiemeCodon_Position/PhymmBL/*.txt ]
then 
  mv `/home/erin/Ruti/TroisiemeCodon_Position/PhymmBL/*.txt output/.` #Move all txt files from PhymmBL to output directory (in working directory)
fi
}
#-------------------------------------------------------------------#


#-------------------------------------------------------------------#
function catFiles {
# This function will 
#1. Accept a user input file (e.g. results.03.phymmBL____Dinsdale_Line_Islands_Christmas_Reef_PhymmBL_4440041_3_XmasLIMic080505_5_fa.txt)
#2. Cat all the results files together 
#	i. Keep initial line but remove dups of QUERY_ID       BEST_MATCH      SCORE   GENUS   GENUS_CONF      FAMILY  FAMILY_CONF     ORDER   ORDER_CON       CLASS   CLASS_CONF      PHYLUM  PHYLUM_CONF     GC_1    GC_2    GC_3    GC_overall

base_fileName=${fileName2:0:-9}
export base_fileName

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
sortedPhylumFile="phylum_sorted_"$partial_dir"_"$fileName_noExt".txt"
export sortedPhylumFile
#echo $sortedPhylumFile

#command below assumes that the phylum will always be classified. #NF is the number of fields
#echo "Phylum   Confidence     GC_1 GC_2 GC_3 GC_overall     ID" > $sortedPHylumFile
awk '$1 ~ /^>/  && $(NF - 4) >= 0.8 {print $(NF - 5), $(NF - 4), $(NF - 3), $(NF - 2), $(NF - 1), $NF, $1}' $completeClassifiedFilePath | sort > $sortedPhylumFile 
#awk '$1 ~ /^>/  && $(NF - 4) >= 0.8 {print; for(i=1; i <2; i++) {getline; print} i=1}' $completeClassifiedFilePath | sort > /home/erin/Ruti/TroisiemeCodon_Position/80Classified/"80_"$completeClassifiedFilePath

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

numArray=('00' '01' '02' '03' '04' '05' '06' '07' '08' '09' '10' '11' '12' '13' '14' '15' '16' '17' '18' '19' '20' '21' '22' '23' '24' '25' '26' '27' '28' '29' '30' '31' '32' '33' '34' '35' '36' '37' '38' '39' '40' '41' '42' '43' '44' '45' '46' '47' '48' '49' '50' '51' '52' '53' '54' '55' '56' '57' '58' '59' '60' '61' '62' '63')
#echo ${numArray[1]}

#_-----------------FUNCTION CALLS-----------------------------------#
splitFiles #call splitFiles function
#dirpath=$PWD #copy name of working directory (containing split fasta files)
#scoreReads
#makeDirectory
#moveFiles #114
#catFiles #138
#Classified_Troiseme_GC #154
#outputFileName='classified_GC_'$fileName #get name of classified file
#checkFileLength #172
#awkCommand #191
#uniquePhyla #212
#comparePhyla
#cp phyla_comparison.sh /home/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/.
#rm /home/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/merged_phyla.txt
#sh /home/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/phyla_comparison.sh
#mv /home/erin/Ruti/TroisiemeCodon_Position/PhymmBL/*.txt output/.
#mv results.03.phymmBL*.txt output/. #This is to ensure that when more than when more than one fasta file in the same directory is to be analyzed, the correct name is copied. 
#-------------------------------------------------------------------#

exit $?
