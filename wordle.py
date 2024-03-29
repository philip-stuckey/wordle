#!/usr/bin/python3 -u
from random import choice
from pathlib import Path
from sys import stdin, stdout, stderr
from argparse import ArgumentParser

def word_list(path):
	return Path(path).read_text().split()


def word_delta(word1, word2):
	return ''.join(
		g if g==l else
		'+' if g in word2 else
		'-' for (g,l) in zip(word1, word2)
	)

def main(word, word_list, max_guesses):
	word = word if word is not None else choice(word_list).strip()

	for i in range(max_guesses):
		guess=''
		while True:
			print(f'{i}/{max_guesses}:', end='', file=stderr)
			stderr.flush()
			guess = stdin.readline().strip()
			if guess not in word_list:
				print(f"'{guess}' not in word list", file=stderr)
				return
			else:
				break

		if guess == word:
			print("you win!", file=stderr)
			break

		print(word_delta(guess, word), file=stdout)
		stdout.flush()

	print("secret word:", word, file=stderr)


if __name__ == '__main__':
	parser = ArgumentParser()
	parser.add_argument('-w', '--word', dest="word")
	parser.add_argument('-n', '--guesses', type=int, dest="max_guesses", default=6)
	parser.add_argument(
		'-f',
		type=word_list,
		default='wordles.txt',
		dest='word_list'
	)
	args = parser.parse_args()
	main(**vars(args))
