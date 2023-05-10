#!/bin/bash

for file in ../data/*.wav
do
	filename=$(basename "$file")
	# echo $filename
	python -u speaker_ident_test.py $file
done