#!/usr/bin/env python3
from random import choice
from pathlib import Path
from sys import stdin, stdout, stderr


def word_delta(word1, word2):
	return ''.join(
		g if g==l else
		'+' if g in word2 else
		'-' for (g,l) in zip(word1, word2)
	)

def main():
	word_list = Path('dict').read_text().split()
	word = choice(word_list).strip()

	for i in range(6):
		guess=''
		while True:
			print(f'{i}/6:', end='', file=stderr)
			stderr.flush()
			guess = stdin.readline().strip()
			if guess not in word_list:
				print(f"'{guess}' not in word list", file=stderr)
			else:
				break

		print(word_delta(guess, word), file=stdout)
		if guess == word:
			print("you win!", file=stderr)
			break

	print(word)

if __name__ == '__main__':
	main()
