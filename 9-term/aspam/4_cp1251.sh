#!/bin/bash
# set -x

file="BurmistrovSanduleanu2012SpamText_cp1251.tex"
>$file
for line in $(cat <BurmistrovSanduleanu2012SpamText.tex | sed 's|utf8|cp1251|g' | sed 's|%.*$||g')
do
	# echo $line
    if [ "${line:1:5}" = "input" ]; then
    	# f =
    	echo " " >>$file
    	cat $(echo $line | sed 's|\\input{||' | sed 's|}||' |sed 's|.tex||'| awk '{print $1".tex"}') >>$file
    	echo " " >>$file
    else
    	printf "%s " $line >>$file
    	echo " " >>$file
    fi
done