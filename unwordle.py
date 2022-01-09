#!python3
from wordle import word_delta
from pathlib import Path
from sys import stdin, stdout, stderr


def count_unique_results(word, word_list):
	return len(set(map(lambda w: word_delta(word, w), word_list)))

def unwordle(word_list, guess="tares", score=count_unique_results, input=stdin, output=stdout):
	print(guess, file=output)
	for result in input:
		word_list = list(filter(lambda w: word_delta(guess, w) == result.strip(), word_list))
		guess = max(word_list, key = lambda w: score(w, word_list))
		print(guess, file=output)

if __name__ == '__main__':
	wordlist = Path('dict').read_text().split()
	unwordle(wordlist)
