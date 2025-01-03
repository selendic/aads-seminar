from typing import Union

from trie.patricia import PatriciaTrie
from trie.prefix import PrefixTrie


def insert_sample_small(t: Union[PrefixTrie, PatriciaTrie]):
	s = """
		baking pancakes making bacon pancake 
		"""
	for word in s.split():
		t.insert(word)


def insert_sample_large(t: Union[PrefixTrie, PatriciaTrie]):
	s = """
		baking pancakes making bacon pancakes take some bacon and Ill put it in a pancake
		bacon pancakes thats what its gonna make bacon pancaaaakes
		"""
	for word in s.split():
		t.insert(word)


def delete_some_words(t: Union[PrefixTrie, PatriciaTrie]):
	t.remove("making")
	t.remove("bacon")
	t.remove("pancake")
	t.remove("its")
	t.remove("gonna")
	t.remove("make")


if __name__ == "__main__":
	trie = PrefixTrie()
	insert_sample_small(trie)
	trie.visualize(file_name="prefix_trie_small_after_insertion", view=False)
	delete_some_words(trie)
	trie.visualize(file_name="prefix_trie_small_after_deletion", view=False)

	trie = PatriciaTrie()
	insert_sample_small(trie)
	trie.visualize(file_name="patricia_trie_small_after_insertion", view=False)
	delete_some_words(trie)
	trie.visualize(file_name="patricia_trie_small_after_deletion", view=False)

	trie = PrefixTrie()
	insert_sample_large(trie)
	trie.visualize(file_name="prefix_trie_large_after_insertion", view=False)
	delete_some_words(trie)
	trie.visualize(file_name="prefix_trie_large_after_deletion", view=False)

	trie = PatriciaTrie()
	insert_sample_large(trie)
	trie.visualize(file_name="patricia_trie_large_after_insertion", view=False)
	delete_some_words(trie)
	trie.visualize(file_name="patricia_trie_large_after_deletion", view=False)
