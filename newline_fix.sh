#!/bin/bash

# This function fixes files if they do not end with a \n character.
function fix_newline {
last_char=$(tail -c 1 "$1"; printf x); 
last_char=${last_char%x}

if [ "$last_char" != $'\n' ]; then
  printf "\n" >> $filename
fi
}
