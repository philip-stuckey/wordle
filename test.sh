#!/usr/bin/bash

rm result;

while read word
do
	mkfifo result
	./unwordle.py -g tears < result | ./wordle.py -w $word -n 100 >> result
	rm result;
	sleep 0.125
done < wordles.txt
