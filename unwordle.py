#!/usr/bin/python3 -u
from wordle import word_delta
from pathlib import Path
from sys import stdin, stdout, stderr
from argparse import ArgumentParser

def count_unique_results(word, word_list):
	return len(set(map(lambda w: word_delta(word, w), word_list)))

def score(word, word_list):
	return count_unique_results(word,word_list)

def unwordle(word_list, guess, score=count_unique_results, input=stdin, output=stdout):
	if guess is None:
		guess = max(word_list, key=lambda w: score(w,word_list))

	print(guess, file=output)
	output.flush()
	for result in input:
		word_list = list(filter(lambda w: word_delta(guess, w) == result.strip(), word_list))
		guess = max(word_list, key = lambda w: score(w, word_list))
		print(guess, file=output)

if __name__ == '__main__':
	def word_list(path):
		return Path('dict').read_text().split()

	parser = ArgumentParser()
	parser.add_argument('-g', '--guess', dest="guess")
	parser.add_argument('-f', '--word-list', dest="word_list", default='wordles.txt', type=word_list)
	args = parser.parse_args()
	unwordle(**vars(args))
