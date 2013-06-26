#!/bin/bash

scriptPathway="/home/erin/Ruti/TroisiemeCodon_Position"

function get_ftpFiles {
#    change the working directory to /home/erin/Ruti/TroisiemeCodon_Position/PhymmBL/
#    using seq, it will call the scoreReads.pl script with the appropriate file name
echo "Do you need to download files from the MG-Rast FTP site? (Y/N followed by [ENTER]:"
read downloadResponse 

if [ $downloadResponse = "y" ] || [ $downloadResponse = "Y" ] || [ $downloadResponse = "yes" ] || [ $downloadResponse = "Yes" ]
then

	awk '{print $NF}' text > folder

	echo "Enter the project number for MG-Rast (followed by [ENTER]):"
	read projectNumber

	partial_wgetCall="ftp://ftp.metagenomics.anl.gov/projects/"$projectNumber"/"
	fileName="299.screen.passed.fna.gz"
	wgetFile="wgetFiles.sh"
	folderFile="folder"
	extension=".fna.gz"
	wget="wget"
	processed="processed/"

	python $scriptPathway/ftp_getFiles.py $partial_wgetCall $fileName $wgetFile $folderFile $extension $processed $wget
	sh $wgetFile 
	rm text
fi
}

get_ftpFiles
sh $scriptPathway/ftp_fileProcessor.sh
python $scriptpathway/ftp_concatenateLines.py
