import cProfile
import pstats
from io import StringIO

from benchmark.config import DATASET_PATH, PROFILE_OUTPUT_PATH
from benchmark.run_experiments import Length
from benchmark.util import load_word_list
from trie import PrefixTrie, PatriciaTrie


def profile_function(func, *args, **kwargs):
	"""
	Profile a given function and return the profiling results as a string.
	:param func: Function to profile.
	:param args: Arguments to the function.
	:param kwargs: Keyword arguments to the function.
	:return: Tuple of the function result and the profiling results.
	"""
	profiler = cProfile.Profile()
	profiler.enable(subcalls=False)
	result = func(*args, **kwargs)
	profiler.disable()

	# Capture profiling stats to a string
	stream = StringIO()
	stats = pstats.Stats(profiler, stream=stream)
	stats.strip_dirs()
	stats.sort_stats(pstats.SortKey.TIME)  # Sort by time
	stats.print_stats()
	return result, stream.getvalue()


def run_experiments_with_profiling(trie_class, words, prefixes, output_file=None):
	"""
	Run profiling experiments with the given trie class.
	:param trie_class: Trie implementation (PrefixTrie or PatriciaTrie).
	:param words: Dataset of words.
	:param prefixes: Dataset of prefixes for range search.
	:param output_file: Output file path for the profiling results. None for console output.
	"""

	def write_to_output(content: str, append: bool = True):
		if output_file:
			with open(output_file, "a" if append else "w") as file:
				file.write(content)
		else:
			print(content)

	write_to_output(f"Profiling {trie_class.__name__}...\n", append=False)

	# Initialize the trie
	trie = trie_class()

	# Experiment 1: Insertion
	_, insert_profile = profile_function(
		lambda: [trie.insert(word) for word in words]
	)
	write_to_output(f"\nInsertion profiling for {trie_class.__name__}:\n\n{insert_profile}\n")

	# Experiment 2: Search
	_, search_profile = profile_function(
		lambda: [trie.search(word) for word in words]
	)
	write_to_output(f"\nSearch profiling for {trie_class.__name__}:\n\n{search_profile}\n")

	# Experiment 3: Range search
	_, range_search_profile = profile_function(
		lambda: [trie.range_search(prefix) for prefix in prefixes]
	)
	write_to_output(f"\nRange search profiling for {trie_class.__name__}:\n\n{range_search_profile}\n")

	# Experiment 4: Deletion
	_, delete_profile = profile_function(
		lambda: [trie.remove(word) for word in words]
	)
	write_to_output(f"\nDeletion profiling for {trie_class.__name__}:\n\n{delete_profile}\n")


if __name__ == "__main__":
	word_list, prefix_list = load_word_list(DATASET_PATH(Length.ALL.value))
	for trie_type in [PrefixTrie, PatriciaTrie]:
		output_path = f"{PROFILE_OUTPUT_PATH}{trie_type.__name__}_output.txt"
		run_experiments_with_profiling(trie_type, word_list, prefix_list, output_file=output_path)
