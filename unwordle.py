#!/usr/bin/python3 -u
from wordle import word_delta
from pathlib import Path
from sys import stdin, stdout, stderr
from argparse import ArgumentParser
from statistics import mean

def freq(data):
	return [sum(map(lambda x: x==y, data)) for y in set(data)]

def negative_mean_group_size(word, word_list):
	return -mean(freq(list(map(lambda w: word_delta(word, w), word_list))))

def count_unique_results(word, word_list):
	return len(set(map(lambda w: word_delta(word, w), word_list)))

def score(word, word_list):
	return negative_mean_group_size(word, word_list)
#	return count_unique_results(word,word_list)

def unwordle(word_list, guess, score=count_unique_results, input=stdin, output=stdout):

	def try_word(word):
		print(word, file=output)
		output.flush()

	if guess is None:
		guess = max(word_list, key=lambda w: score(w,word_list))

	try_word(guess)

	guesses=1
	candidates = word_list.copy()

	for result in input:
		if result == guess:
			output.flush()
			output.close()
			return (guess, guesses)

		candidates = list(filter(lambda w: word_delta(guess, w) == result.strip(), candidates))
		if len(candidates) == 1:
			try_word(candidates[0])
			continue

		if not candidates:
			return ("failed", -1)

		guess = max(word_list, key = lambda w: score(w, candidates))
		try_word(guess)
		guesses += 1
	output.close()

	return (guess, guesses)

if __name__ == '__main__':
	def word_list(path):
		print(path, file=stderr)
		return Path('dict').read_text().split()

	parser = ArgumentParser()
	parser.add_argument('-g', '--guess', dest="guess")
	parser.add_argument('-f', '--word-list', dest="word_list", default='wordles.txt', type=word_list)
	args = parser.parse_args()
	print(*unwordle(**vars(args)), file=stderr)
