#!/usr/bin/python3 -u
from random import choice
from pathlib import Path
from sys import stdin, stdout, stderr
from argparse import ArgumentParser


def word_delta(word1, word2):
	return ''.join(
		g if g==l else
		'+' if g in word2 else
		'-' for (g,l) in zip(word1, word2)
	)

def main(word, word_list, max_guesses):
	word_list = Path('dict').read_text().split()
	word = word if word is not None else choice(word_list).strip()

	for i in range(max_guesses):
		guess=''
		while True:
			print(f'{i}/6:', end='', file=stderr)
			stderr.flush()
			guess = stdin.readline().strip()
			if guess not in word_list:
				print(f"'{guess}' not in word list", file=stderr)
				return
			else:
				break

		print(word_delta(guess, word), file=stdout)
		stdout.flush()
		if guess == word:
			print("you win!", file=stderr)
			break

	print(word, file=stdout)
	stdout.close()

if __name__ == '__main__':
	parser = ArgumentParser()
	parser.add_argument('-w', '--word', dest="word")
	parser.add_argument('-n', '--guesses', type=int, dest="max_guesses", default=6)
	parser.add_argument(
		'-f',
		type=lambda x: Path(x).read_text().split(),
		default='wordles.txt',
		dest='word_list'
	)
	args = parser.parse_args()
	main(**vars(args))
