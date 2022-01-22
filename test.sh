#!/usr/bin/bash

test -p result && rm result;
echo "generating first guess (this may take some time)"

firstguess=$(./unwordle.py < /dev/null 2> /dev/null | head -n1)
echo $firstguess

while read word
do
	mkfifo result
	./unwordle.py -g $firstguess < result | ./wordle.py -w $word -n 100  >> result 2> /dev/null
	rm result;
	sleep 0.125
done < wordles.txt
