#!/bin/bash

scriptPathway="/home/erin/Ruti/TroisiemeCodon_Position"
metaDataPathway="/home/erin/Ruti/TroisiemeCodon_Position/ENVIRONMENTS/MetaData"

wget="wget"
wgetCall="http://metagenomics.anl.gov/metagenomics.cgi?page=DownloadMetagenome&action=download_md&filename=mgm"
wgetFile="wget_metaFiles.sh"
metaExtension=".metadata.txt"
fileExt=".txt"
Oh="-O"
folder="folder"

echo "Enter the filename to store the contents of this directory (followed by [ENTER]):"
read fileName 

fileName=$fileName".text"
sed '/[a-zA-Z]/d' $folder > $fileName #remove any line that does not begin with a number
python $scriptPathway/meta_getFiles.py $wget $wgetCall $wgetFile $metaExtension $fileExt $Oh $fileName
cp $wgetFile $metaDataPathway/$wgetFile
cp $fileName $metaDataPathway/$fileName
cd $metaDataPathway 

echo "Do you need to download files from the MG-Rast FTP site? (Y/N followed by [ENTER]):"
read downloadResponse

if [ $downloadResponse = "y" ] || [ $downloadResponse = "Y" ] || [ $downloadResponse = "yes" ] || [ $downloadResponse = "Yes" ]
then
	sh $wgetFile
fi

rm $wgetFile
dirpath=$PWD
python $scriptPathway/meta_extractData.py $PWD
