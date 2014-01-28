#!/bin/bash
CURR_DIR=$(pwd)
for file in $(find $CURR_DIR -name "*.png")
do
	echo $file
	optipng -o4 -quiet -preserve "$file"
done
