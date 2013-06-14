#!/bin/bash 

#-------------------------------------------------------------------#
function splitFiles {

# splitFiles will 
#1. Accept a user input file (e.g. fileName)
#2  Accept a user input for the number of processors to use (e.g. processors)
#2. Split the file into smaller sizes based on number of processors used and where the number of lines in each part is equally divisible by 2. 

echo "Enter the name of the fasta file to split into parts (followed by [ENTER]):"
read fileName #e.g. 4502935.3.fa
#echo $fileName
export fileName #this makes it available to other functions
echo "How many processors do you want to use? (followed by [ENTER])?:"
read processors
export processors #this makes it available to other functions

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
}
#-------------------------------------------------------------------#


#-------------------------------------------------------------------#
function scoreReads {
#scoreReads will
#    change the working directory to /data/erin/Ruti/TroisiemeCodon_Position/PhymmBL/
#    using seq, it will call the scoreReads.pl script with the appropriate file name
echo "Do you want to classify the reads? (Y/N followed by [ENTER]:"
read scoreRead_Response 

if [ $scoreRead_Response = "y" ] || [ $scoreRead_Response = "Y" ] || [ $scoreRead_Response = "yes" ] || [ $scoreRead_Response = "Yes" ] 
then

	cd $PhymmBL_directory 

	echo "What type of sequencing method was used?"
	echo -n '
	454 = 0
	Illumina = 1
	Sanger = 2
	Other = 3'

	read sequencing_number
	sequencing_type="sequencing_type"

	while [ "$sequencing_number" != 0 ] or [ "$sequencing_number" != 1 ] or [ "$sequencing_number" != 2 ] or [ "$sequencing_number" != 3 ] ; do 
		echo "What type of sequencing method was used?"
		echo -n '
		454 = 0
		Illumina = 1
		Sanger = 2
		Other = 3'
	read sequencing_number
	done

	if [ "$sequencing_number" == 0 ]; then
		seq -w 0 $(($processors-1)) | parallel ./scoreReads.pl $dirpath/$fileName_noExt'_'{}'.fa'
		sequencing_type="454"
	elif [ "$sequencing_number" == 1 ]; then
		seq -w 0 $(($processors-1)) | parallel ./scoreReads.pl $dirpath/$fileName_noExt'_'{}'.fa'
		sequencing_type="illumina"
	elif [ "$sequencing_number" == 2 ]; then
		seq -w 0 $(($processors-1)) | parallel ./scoreReads.pl $dirpath/$fileName_noExt'_'{}'.fa'
		sequencing_type="Sanger"
	elif [ "$sequencing_number" == 3 ]; then
		seq -w 0 $(($processors-1)) | parallel ./scoreReads.pl $dirpath/$fileName_noExt'_'{}'.fa'
		sequencing_type="other"
	fi

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
#Purpose: Move specific text files from PhymmBL dir to output directory in current working 
#    directory. Moved files are specific to files in working directory.

#python /data/erin/Ruti/TroisiemeCodon_Position/moveResultFiles.py $PWD $PhymmBL_directory $Environment_directory

declare -a resultFiles=(`ls $outputDirectory/$resultsPrefix`) 
cp ${resultFiles[@]} .  
declare -a resultFiles=(`ls $PWD/$resultsPrefix`) 
fileName2=$resultFiles[2]
#echo "fileName2 is $fileName2"
export fileName2
}
#-------------------------------------------------------------------#


#-------------------------------------------------------------------#
function catFiles {
# This function will 
#1. Accept a user input file (e.g. results.03.phymmBL____Dinsdale_Line_Islands_Christmas_Reef_PhymmBL_4440041_3_XmasLIMic080505_5_fa.txt)
#2. Cat all the results files together 
#	i. Keep initial line but remove dups of QUERY_ID       BEST_MATCH      SCORE   GENUS   GENUS_CONF      FAMILY  FAMILY_CONF     ORDER   ORDER_CON       CLASS   CLASS_CONF      PHYLUM  PHYLUM_CONF     GC_1    GC_2    GC_3    GC_overall

lengthA=$(expr length $PWD) 
#base_fileName=${fileName2:$lengthA:-12} #this needs to be to 12 when there is file_1 rather than file_01 
base_fileName=${fileName2:0:-11}
export base_fileName

echo "QUERY_ID  BEST_MATCH     SCORE     GENUS     GENUS_CONF     FAMILY    FAMILY_CONF    ORDER     ORDER_CONF     CLASS     CLASS_CONF     PHYLUM    PHYLUM_CON" > $base_fileName'fa.txt'

#for i in `seq -w 0 $(($processors - 1))`; do 
#for i in `seq -w 1 $processors `; do 
for i in `seq -w 1 $(($processors - 0))`; do 
	sed 1d $base_fileName$i'_fa.txt' >> $base_fileName'fa.txt' 
done;
#cat $base_fileName'1_fa.txt' <(sed 1d $base_fileName'2_fa.txt') <(sed 1d $base_fileName'3_fa.txt') <(sed 1d $base_fileName'4_fa.txt') <(sed 1d $base_fileName'5_fa.txt') <(sed 1d $base_fileName'6_fa.txt') > $base_fileName'fa.txt'
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

#python /data/erin/Ruti/TroisiemeCodon_Position/Classified_Troiseme_GC.py $fileName $base_fileName'fa.txt' $outputFileName
python $scriptPathway/Classified_Troiseme_GC.py $fileName $base_fileName'fa.txt' $outputFileName
#python /data/erin/Ruti/TroisiemeCodon_Position/Classified_Troiseme_GC.py $fileName $outputFileName
}
#-------------------------------------------------------------------#


#-------------------------------------------------------------------#
function checkFileLength {
#verify # of lines in classified_GC.. file is 1 (ONE) greater than
#original unsplit fasta file (there is an initial & additional header file in classified_GC...

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

#command below works only when bacteria is classified at each level (phylum-genus)
#awk '$1 ~ /^>/  && NF == 17 {print $(NF - 5), $(NF - 4), $(NF - 3), $(NF - 2), $(NF - 1), $NF}' $completeClassifiedFilePath | sort > $sortedPhylumFile 
awk '$1 ~ /^[A-Z]/  {print $0}' $sortedPhylumFile > tempFile.txt #This will copy lines that start with a letter into tempFile
mv tempFile.txt $sortedPhylumFile
#cp $sortedPhylumFile /data/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/. 
cp $sortedPhylumFile $scriptPathway/Sorted_Phylum/. 
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

#------------------VARIABLE DEFINITIONS & FUNCTION CALLS-----------------------------------#
dirpath=$PWD #copy name of working directory (containing split fasta files)
outputDirectory=$PWD"/output"
PhymmBL_directory="/data/erin/Ruti/TroisiemeCodon_Position/PhymmBL"
Environment_directory="/data/erin/Ruti/TroisiemeCodon_Position/ENVIRONMENTS/"
resultsPrefix="results.03.phymmBL*.txt"
scriptPathway="/data/erin/Ruti/TroisiemeCodon_Position"
splitFiles
outputFileName='classified_GC_'$fileName #get name of classified file
scoreReads
makeDirectory
moveFiles 
catFiles 
Classified_Troiseme_GC 
checkFileLength 
awkCommand
uniquePhyla 
comparePhyla
cp phyla_comparison.sh /home/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/.

#rm /home/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/merged_phyla.txt
#sh /home/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/phyla_comparison.sh
#mv /home/erin/Ruti/TroisiemeCodon_Position/PhymmBL/*.txt output/.
#mv results.03.phymmBL*.txt output/. #This is to ensure that when more than when more than one fasta file in the same directory is to be analyzed, the correct name is copied. 
#-------------------------------------------------------------------#

exit $?
