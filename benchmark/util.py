import os
import sys


def load_word_list(file_path) -> list[str]:
	"""
	Load and preprocess a word list from a text file.
	Each word should be on a separate line.
	Also, prepare the prefixes for range search.
	:param file_path: Path to the word list file.
	:return: List of words and prefixes.
	"""
	if not os.path.exists(file_path):
		raise FileNotFoundError(f"File not found: {file_path}")

	with open(file_path, "r") as file:
		words = [line.strip() for line in file.readlines()]

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
