#!/usr/bin/bash
wordle=$(mktemp)
cp ./wordle.py $wordle
chmod +x $wordle

unwordle=$(mktemp)
cp ./unwordle.jl $unwordle
chmod +x $unwordle

set -o pipefail
test -p result && rm result;
echo "# generating first guess (this may take some time)"

firstguess=$(./unwordle.jl < /dev/null 2> /dev/null | head -n1)
echo "# first guess $firstguess"

while read word
do
	# echo "# $word"
	mkfifo result-julia
	$unwordle -g $firstguess < result-julia | $wordle -w $word -n 100  >> result-julia 2> /dev/null || break
	rm result-julia
	sleep 0.125
done < wordles.txt
