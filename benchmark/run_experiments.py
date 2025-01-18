import time
import tracemalloc
from enum import Enum
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from benchmark.config import DATASET_PATH, CSV_PATH, PLOT_PATH, INCREMENTAL_SIZES
from benchmark.util import load_word_list
from trie import PrefixTrie, PatriciaTrie


def measure_time_and_memory(func, *args, **kwargs):
	"""
	Measure execution time and peak memory usage of a function.
	:param func: Function to measure.
	:param args: Non-keyword function arguments.
	:param kwargs: Keyword function arguments.
	:return: Function result, execution time, peak memory usage (in KB).
	"""
	tracemalloc.start()
	start_time = time.perf_counter()
	result = func(*args, **kwargs)
	end_time = time.perf_counter()
	_, peak_memory = tracemalloc.get_traced_memory()
	tracemalloc.stop()
	return result, end_time - start_time, peak_memory / 1024


def experiment_with_trie(trie_class, words, prefixes_for_range_search):
	"""
	Run an experiment with a given trie implementation and log the results.
	:param trie_class: Trie class to use (PrefixTrie or PatriciaTrie).
	:param words: List of words to use.
	:param prefixes_for_range_search: List of prefixes to use for range search.
	:return: Dictionary of results for insertion, search, range search and deletion.
	"""
	results = {}

	# Initialize the trie
	trie = trie_class()

	# Experiment 1: Insertion
	_, time_insert, memory_insert = measure_time_and_memory(
		lambda: [trie.insert(word) for word in words]
	)
	results["Insertion"] = {"Time": time_insert, "Memory": memory_insert}

	# Experiment 2: Search
	_, time_search, memory_search = measure_time_and_memory(
		lambda: [trie.search(word) for word in words]
	)
	results["Search"] = {"Time": time_search, "Memory": memory_search}

	# Experiment 3: Range search
	_, time_range_search, memory_range_search = measure_time_and_memory(
		lambda: [trie.range_search(prefix) for prefix in prefixes_for_range_search]
	)
	results["Range_search"] = {"Time": time_range_search, "Memory": memory_range_search}

	# Experiment 4: Deletion
	_, time_delete, memory_delete = measure_time_and_memory(
		lambda: [trie.remove(word) for word in words]
	)
	results["Deletion"] = {"Time": time_delete, "Memory": memory_delete}

	return results


class Length(Enum):
	"""
	Enum class for different sizes of the dataset.
	"""
	ALL = ""
	SHORT = "-short"
	MEDIUM = "-medium"
	LONG = "-long"


def run_experiments(length: Length = Length.ALL):
	"""
	Run experiments with the given dataset length.
	Save the results to a CSV file and plot the performance.
	:param length: Word length of the dataset (ALL, SHORT, MEDIUM, LONG).
	:return: Pandas DataFrame containing the experiment results.
	"""
	# Load and preprocess the dataset
	print("Loading and preprocessing the dataset...")
	words, prefixes_for_range_search = load_word_list(DATASET_PATH(length.value))
	# words = filter_words_by_length(words, MIN_WORD_LENGTH, MAX_WORD_LENGTH)

	# Future DataFrame to store the results
	results = []

	# Run experiments for incremental dataset sizes
	for size in INCREMENTAL_SIZES:
		# print(f"\n=== Experiment with {size} words ===")
		subset_words = words[:size]

		for trie_class in [PrefixTrie, PatriciaTrie]:
			trie_results = experiment_with_trie(trie_class, subset_words, prefixes_for_range_search)
			for operation, metrics in trie_results.items():
				results.append({
					"Trie": trie_class.__name__,
					"Size": size,
					"Operation": operation,
					"Time": metrics["Time"],
					"Memory": metrics["Memory"]
				})

	# Convert the results to a DataFrame
	results_df = pd.DataFrame(results)

	# Save the results to a CSV file
	csv_file_name = f"{CSV_PATH}experiment_results.csv"  # f"{CSV_PATH}experiment_results_{length.name.lower()}.csv" if filtering based on word length
	file_path = Path(csv_file_name)
	file_path.parent.mkdir(parents=True, exist_ok=True)
	results_df.to_csv(csv_file_name, index=False)
	print(f"Results saved to {csv_file_name}")

	# Plot the results
	plot_results(results_df, length)


def plot_results(df, length: Length = Length.ALL):
	"""
	Create performance plots from the experiment results.
	:param df: Pandas DataFrame containing the experiment results.
	:param length: Word length of the dataset (ALL, SHORT, MEDIUM, LONG).
	"""
	for operation in df["Operation"].unique():
		for metric, marker, y_label in zip(["Time", "Memory"], ["o", "s"], ["Time (s)", "Memory (KB)"]):
			plt.figure(figsize=(12, 6))
			for trie in df["Trie"].unique():
				subset = df[(df["Trie"] == trie) & (df["Operation"] == operation)]
				plt.plot(
					subset["Size"],
					subset[metric],
					marker=marker,
					linestyle="--",
					label=f"{trie}"
				)
			plt.title(
				f"{operation} {metric.lower()} performance", fontsize=20
			)  # f"{operation} {metric.lower()} performance ({length.name.lower()} words)" if filtering based on word length
			plt.xlabel("Dataset size", fontsize=16)
			plt.ylabel(y_label, fontsize=16)
			plt.legend(loc="best", fontsize=14)
			plt.grid(True)
			file_path = f"{PLOT_PATH}{operation.lower()}_{metric.lower()}_performance.png"  # f"{PLOT_PATH}{operation.lower()}_{metric.lower()}_performance_{length.name.lower()}.png" if filtering based on word length
			file_path = Path(file_path)
			file_path.parent.mkdir(parents=True, exist_ok=True)
			plt.savefig(file_path)
			print(f"Saved {file_path}")
			plt.show()


if __name__ == "__main__":
	run_experiments()
