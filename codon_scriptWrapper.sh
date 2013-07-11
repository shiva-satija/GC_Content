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

echo "Do you want to split the files? (Y/N followed by [ENTER]:"
read split_Response 

if [ $split_Response = "y" ] || [ $split_Response = "Y" ] || [ $split_Response = "yes" ] || [ $split_Response = "Yes" ] 
then
	if [ $processors -ne 1 ]
	then 
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
	fi
fi
}
#-------------------------------------------------------------------#


#-------------------------------------------------------------------#
function scoreReads {
#scoreReads will
#    change the working directory to /home/erin/Ruti/TroisiemeCodon_Position/PhymmBL/
#    using seq, it will call the scoreReads.pl script with the appropriate file name
echo "Do you want to classify the reads? (Y/N followed by [ENTER]:"
read scoreRead_Response 
export scoreRead_Repsonse

if [ $scoreRead_Response = "y" ] || [ $scoreRead_Response = "Y" ] || [ $scoreRead_Response = "yes" ] || [ $scoreRead_Response = "Yes" ] 
then
	cd $PhymmBL_directory 

	if [ $processors -ne 1 ]
	then 
		seq -w 00 $(($processors-1)) | parallel ./scoreReads.pl $dirpath/$fileName_noExt'_'{}'.fa'

	else 
		./scoreReads.pl $dirpath/$fileName
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

if [ $scoreRead_Response = "y" ] || [ $scoreRead_Response = "Y" ] || [ $scoreRead_Response = "yes" ] || [ $scoreRead_Response = "Yes" ] 
then 
	python $scriptPathway/moveResultFiles.py $PWD $PhymmBL_directory $Environment_Directory $errFile $rawBlastOutput $rawPhymmOutput $results1 $results2 $results3 $tempRev $fileName_noExt
fi
}
#-------------------------------------------------------------------#


#-------------------------------------------------------------------#
function catFiles {
# This function will 
#1. Accept a user input file (e.g. results.03.phymmBL____Dinsdale_Line_Islands_Christmas_Reef_PhymmBL_4440041_3_XmasLIMic080505_5_fa.txt)
#2. Cat all the results files together 
#	i. Keep initial line but remove dups of QUERY_ID       BEST_MATCH      SCORE   GENUS   GENUS_CONF      FAMILY  FAMILY_CONF     ORDER   ORDER_CON       CLASS   CLASS_CONF      PHYLUM  PHYLUM_CONF     GC_1    GC_2    GC_3    GC_overall

echo "Do you want to concatenate the result files? (Y/N followed by [ENTER]:"
read catFiles_Response 
if [ $catFiles_Response = "y" ] || [ $catFiles_Response = "Y" ] || [ $catFiles_Response = "yes" ] || [ $catFiles_Response = "Yes" ] 
	then 
	declare -a resultFiles=(`ls $outputDirectory/$resultsPrefix`) 

	if [ $processors -eq 1 ]
	then 
		cp $outputDirectory/$resultFiles ../$concat_resultFile
	fi

	if [ $processors -ne 1 ]
	then 
		cd $outputDirectory
		fileName2=$resultFiles[1]
		lengthA=$(expr length $outputDirectory"/") #without removing the"/", it will end up in the base_fileName
		base_fileName=${fileName2:$lengthA:-12} #the -3 removes the [x] from the name

		echo "QUERY_ID  BEST_MATCH     SCORE     GENUS     GENUS_CONF     FAMILY    FAMILY_CONF    ORDER     ORDER_CONF     CLASS     CLASS_CONF     PHYLUM    PHYLUM_CON" > $concat_resultFile

		for i in `seq -w 00 $(($processors - 1))`; do 
			sed 1d $base_fileName$i'_fa.txt' >> $concat_resultFile
		done;

		mv $concat_resultFile ../.
		cd -
	fi
fi
}
#-------------------------------------------------------------------#


#-------------------------------------------------------------------#
function Classified_Troiseme_GC {
#Purpose: To merge classified sequences file to original fasta file into one while calculating the GC% from the 1st, 2nd, and 3rd position for sequences as well as the overal gc content. Data is saved as fasta file.

echo "Do you want to merge the classified files? (Y/N followed by [ENTER]:"
read classify_Response 
export classify_Response

if [ $classify_Response = "y" ] || [ $classify_Response = "Y" ] || [ $classify_Response = "yes" ] || [ $classify_Response = "Yes" ] 
then
	python $scriptPathway/Classified_Troiseme_GC.py $fileName $concat_resultFile $outputFileName
fi
}
#-------------------------------------------------------------------#


#-------------------------------------------------------------------#
function checkFileLength {
#Purpse: Verify the number of lines in classified_GC.. file is 1 (ONE) greater than
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
sortedPhylumFile="phylum_sorted_"$partial_dir$fileName_noExt".txt"
export sortedPhylumFile

#command below assumes that the phylum will always be classified. #NF is the number of fields
#echo "Phylum   Confidence     GC_1 GC_2 GC_3 GC_overall     ID" > $sortedPHylumFile
awk '$1 ~ /^>/  && $(NF - 4) >= 0.8 {print $(NF - 5), $(NF - 4), $(NF - 3), $(NF - 2), $(NF - 1), $NF, $1}' $completeClassifiedFilePath | sort > $sortedPhylumFile 

#command below works only when bacteria is classified at each level (phylum-genus)
#awk '$1 ~ /^>/  && NF == 17 {print $(NF - 5), $(NF - 4), $(NF - 3), $(NF - 2), $(NF - 1), $NF}' $completeClassifiedFilePath | sort > $sortedPhylumFile 
awk '$1 ~ /^[A-Z]/  {print $0}' $sortedPhylumFile > tempFile.txt #This will copy lines that start with a letter into tempFile
mv tempFile.txt $sortedPhylumFile
cp $sortedPhylumFile $sortedPhylumPathway/.
}
#-------------------------------------------------------------------#


#-------------------------------------------------------------------#
function uniquePhyla {
#Purpose: go through sorted file for unique phyla names, append to
#"unique_phyla.txt" (in Sorted_Phylum directory)
# go through text file to ensure unique names exist only

awk '{ print $1}' $sortedPhylumFile | uniq > unique_phyla.txt
cat unique_phyla.txt $sortedPhylumPathway/unique_phyla.txt > $sortedPhylumPathway/temp_unique_phyla.txt
sort $sortedPhylumPathway/temp_unique_phyla.txt > $sortedPhylumPathway/sort_temp_unique_phyla.txt
uniq $sortedPhylumPathway/sort_temp_unique_phyla.txt > $sortedPhylumPathway/unique_phyla.txt
rm  $sortedPhylumPathway/sort_temp_unique_phyla.txt 
rm  $sortedPhylumPathway/temp_unique_phyla.txt 
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
python $scriptPathway/compare_phyla.py $sortedPhylumPathway
}
#-------------------------------------------------------------------#

#------------------VARIABLE DEFINITIONS & FUNCTION CALLS-----------------------------------#
dirpath=$PWD #copy name of working directory (containing split fasta files)
outputDirectory=$PWD"/output"
PhymmBL_directory="/home/erin/Ruti/TroisiemeCodon_Position/PhymmBL"
Environment_directory="/home/erin/Ruti/TroisiemeCodon_Position/ENVIRONMENTS/"
results3Prefix="results.03.phymmBL__*.txt"
results2Prefix="results.02.blast__*.txt"
scriptPathway="/home/erin/Ruti/TroisiemeCodon_Position"
sortedPhylumPathway=$scriptPathway"/Sorted_Phylum/"
splitFiles
outputFileName='classified_GC_'$fileName #get name of classified file
completeClassifiedFilePath=$dirPath$outputFileName
scoreReads
makeDirectory
errFile="errFile"
rawBlastOutput="rawBlastOutput"
rawPhymmOutput="rawPhymmOutput"
results1="results.01.phymm"
results2="results.02.blast"
results3="results.03.phymmBL"
tempRev="tempRev"
resultsPrefix="results.03.phymmBL*.txt"
concat_resultFile=$results3"_"$fileName
#echo $concat_resultFile
#echo $outputFileName

moveFiles 
catFiles 
Classified_Troiseme_GC 
checkFileLength 
awkCommand
uniquePhyla 
comparePhyla
cp phyla_comparison.sh $sortedPhylumPathway/.

cd $sortedPhylumPathway
sh phyla_comparison.sh > /dev/null 2>&1


sort merged_phyla.txt  > temp.txt
mv temp.txt merged_phyla.txt
sed -i '1s/^/Phylum\tOccurances\tConfidernce\tGC_1\tGC_2\tGC_3\tGC_overall\tFilename\n/' merged_phyla.txt
cd -
#-----------------------------------FIN----------------------------------------------#
