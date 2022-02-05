#!/usr/bin/bash

test -p result && rm result;
echo "# generating first guess (this may take some time)"

firstguess=tares  #$(./unwordle.py < /dev/null 2> /dev/null | head -n1)
echo "# first guess $firstguess"

echo word attempts
while read word
do
	# echo "# $word"
	mkfifo result
	./unwordle.py -g $firstguess < result | ./wordle.py -w $word -n 100  >> result 2> /dev/null
	rm result;
	sleep 0.125
done < wordles.txt
