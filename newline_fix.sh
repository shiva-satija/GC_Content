#!/bin/bash
filename="f"

function fix_newline {
last_char=`tail -c 1 $1`

if [[ $last_char='\n' ]]; then
  printf "\n" >> $filename
fi
}
  
fix_newline $filename

