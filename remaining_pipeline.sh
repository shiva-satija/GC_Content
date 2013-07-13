#!/bin/bash

Metadata_directory="/home/erin/Ruti/TroisiemeCodon_Position/ENVIRONMENTS/MetaData/"
sortedPhylum_directory="/home/erin/Ruti/TroisiemeCodon_Position/Sorted_Phylum/"

python remaining_processingList.py $Metadata_directory $sortedPhylum_directory
sh remaining_processingList.sh > remaining_processingList.txt
