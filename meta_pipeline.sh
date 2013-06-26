
scriptPathway="/home/erin/Ruti/TroisiemeCodon_Position"
wget="wget"
wgetCall="http://metagenomics.anl.gov/metagenomics.cgi?page=DownloadMetagenome&action=download_md&filename=mgm"
wgetFile="wget_metaFiles.sh"
metaExtension=".metadata.txt"
fileExt=".txt"
Oh="-O"

python $scriptPathway/meta_getFiles.py $wget $wgetCall $wgetFile $metaExtension $fileExt $Oh

