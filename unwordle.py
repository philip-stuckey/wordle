#!/usr/bin/python3 -u
from wordle import word_delta, word_list
from pathlib import Path
from sys import stdin, stdout, stderr
from argparse import ArgumentParser
from statistics import mean
from math import log

def freq(data):
	return (sum(map(lambda x: x==y, data)) for y in set(data))

def group_sizes(word, word_list):
	return freq(map(lambda w: word_delta(w, word_list)))

def freq_sqr(data):
	return (sum(map(lambda x: x==y, data))**2 for y in set(data))

def entropy(word, word_list):
	W = len(word_list)
	return sum(S/W * log(S/W) for S in group_sizes(word, word_list))

def expected_group_size(word, word_list):
	return mean(freq_sqr(map(lambda w: word_delta(word, w), word_list)))

def max_group_size(word, word_list):
	return max(group_sizes(word, word_list))

def mean_group_size(word, word_list):
	return mean(group_sizes(word, word_list))

def negative_count_unique_results(word, word_list):
	return -len(set(map(lambda w: word_delta(word, w), word_list)))

def debug(*args, file=stderr, **kwargs):
	pass
#	return print(*args, file=file, **kwargs)


def unwordle(
    word_list, 
    guess, 
    score=expected_group_size, 
    input=stdin, 
    output=stdout):
	debug(score)
	def try_word(word):
		print(word, file=output)
		output.flush()

	def pick_word(candidates):
		return min(candidates, key=lambda w: score(w, candidates))

	if guess is None:
		guess = pick_word(word_list)

	try_word(guess)

	guesses=1
	candidates = word_list.copy()

	for result in input:
		candidates = list(filter(lambda w: word_delta(guess, w) == result.strip(), candidates))
		debug(candidates if len(candidates) < 10 else len(candidates))
		if not candidates:
			try_word("tears")
			return ("failed", -guesses)
		elif len(candidates) == 1:
			guess = candidates[0]
		else:
			guess = pick_word(candidates)
		try_word(guess)
		guesses += 1
	output.close()

	return (guess, guesses)

if __name__ == '__main__':
	try:
		import signal
		signal.signal(signal.SIGPIPE, signal.SIG_DFL)
	except (ImportError, AttributeError):
		# Do nothing on platforms without signals or ``SIGPIPE``.
		pass

	parser = ArgumentParser()
	parser.add_argument('-g', '--guess', dest="guess")
	parser.add_argument('-f', '--word-list', dest="word_list", default='wordles.txt', type=word_list)
	args = parser.parse_args()
	print(*unwordle(**vars(args)), file=stderr)
