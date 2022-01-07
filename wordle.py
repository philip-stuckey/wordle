#!/usr/bin/env python3
from random import choice
from pathlib import Path
from sys import stdin, stdout

word_list = Path('dict').read_text().split()
word = choice(word_list).strip()

for i in range(6):
	guess=''
	while True:
		print(f'{i}/6:', end='')
		stdout.flush()
		guess = stdin.readline().strip()
		if guess not in word_list:
			print(f"'{guess}' not in word list")
		else:
			break

	print(*(g if g==l else '+' if g in word else '-' for (g,l) in zip(guess, word)), sep='' )
	if guess == word:
		print("you win!")
		break

print(word)
