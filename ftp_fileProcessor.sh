#!/bin/bash    

#Author: E. Reichenberger
#Created: 5.25.2013

#Purpose: Process downloaded tar.gz files
#    a. get a list of files in directory
#    b. untar files (if tar.gz)
#    c. make directory for each file
#    d. create two sub-directories (Phylum, glimmer-mg) in each directory
#    e. copy untar file into appropriate directory and sub-directories
#    f. this script will also call concateLines.py which will concatenate a unique sequence spread across multiple lines

scriptPathway="/home/erin/Ruti/TroisiemeCodon_Position"
Phylum="Phylum"
Glimmer="glimmer-mg"

for files in `ls *.fna.gz $search_dir`; do
     echo $files
     gunzip fvxz $files
 done

 for files in `ls *.fna $search_dir`; do
      python $scriptPathway/ftp_concatenateLines.py $files
      Directory=${files:0:-4}
      newFile=$Directory'.fa'
      mv $files $newFile
      subdirectory1=$Directory'/'$Phylum
      subdirectory2=$Directory'/'$Glimmer
      
      if [ ! -d "$Directory" ]; then
         mkdir $Directory
      fi

      cd $Directory
      if [ ! -d "$subdirectory1" ]; then
        mkdir $Phylum
      fi

       if [ ! -d "$subdirectory2" ]; then
          mkdir $Glimmer
       fi

      cd -
      cp $newFile $Directory/.
      cp $newFile $subdirectory1/.
      cp $newFile $subdirectory2/.
done


for files in `ls *.fa.gz $search_dir`; do
     echo $files
     gunzip fvxz $files
 done

 for files in `ls *.fa $search_dir`; do
      python $scriptPathway/ftp_concatenateLines.py $files
      Directory=${files:0:-3}
      newFile=$Directory'.fa'
      mv $files $newFile
      subdirectory1=$Directory'/'$Phylum
      subdirectory2=$Directory'/'$Glimmer
      
      if [ ! -d "$Directory" ]; then
         mkdir $Directory
      fi

      cd $Directory
      if [ ! -d "$subdirectory1" ]; then
        mkdir $Phylum
      fi

       if [ ! -d "$subdirectory2" ]; then
          mkdir $Glimmer
       fi

      cd -
      cp $newFile $Directory/.
      cp $newFile $subdirectory1/.
      cp $newFile $subdirectory2/.
done
