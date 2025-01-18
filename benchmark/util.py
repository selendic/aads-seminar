import os
import sys
from typing import Union


def load_word_list(file_path, return_prefix_list: bool = True) -> Union[tuple[list[str], list[str]], list[str]]:
	"""
	Load and preprocess a word list from a text file.
	Each word should be on a separate line.
	Also, prepare the prefixes for range search.
	:param file_path: Path to the word list file.
	:param return_prefix_list: Return the prefixes for range search.
	:return: List of words and prefixes.
	"""
	if not os.path.exists(file_path):
		raise FileNotFoundError(f"File not found: {file_path}")

	with open(file_path, "r") as file:
		words = [line.strip() for line in file.readlines()]

	if return_prefix_list:
		# Prepare the prefixes for range search
		# We will use all possible one-character and two-character prefixes
		ascii_alphabet_lowercase = "abcdefghijklmnopqrstuvwxyz"
		prefixes = [char for char in ascii_alphabet_lowercase]
		prefixes += [char1 + char2 for char1 in ascii_alphabet_lowercase for char2 in
					 ascii_alphabet_lowercase]
		return words, prefixes
	else:
		return words


def filter_words_by_length(words, min_length=1, max_length=sys.maxsize):
	"""
	Filter the words by length.
	:param words: List of words to filter.
	:param min_length: Minimum word length.
	:param max_length: Maximum word length.
	:return: Filtered list of words.
	"""
	return [word for word in words if min_length <= len(word) <= max_length]
