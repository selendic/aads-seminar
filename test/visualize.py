from typing import Union

from src.patricia_tree import PatriciaTree
from src.prefix_tree import PrefixTree


def insert_sample_small(t: Union[PrefixTree, PatriciaTree]):
	s = """
		pancakes pancake
		"""
	for word in s.split():
		t.insert(word)


def insert_sample_large(t: Union[PrefixTree, PatriciaTree]):
	s = """
		Making pancakes makin bacon pancakes take some bacon and Ill put it in a pancake
		bacon pancakes thats what its gonna make bacon pancaaaakes
		"""
	for word in s.split():
		t.insert(word)


def delete_some_words(t: Union[PrefixTree, PatriciaTree]):
	t.remove("makin")
	t.remove("bacon")
	t.remove("pancake")
	t.remove("its")
	t.remove("gonna")
	t.remove("make")


if __name__ == "__main__":
	tree = PrefixTree()
	insert_sample_large(tree)
	tree.visualize(file_name="prefix_tree_after_insertion", view=False)
	delete_some_words(tree)
	tree.visualize(file_name="prefix_tree_after_deletion", view=False)

	tree = PatriciaTree()
	insert_sample_large(tree)
	tree.visualize(file_name="patricia_tree_after_insertion", view=False)
	delete_some_words(tree)
	tree.visualize(file_name="patricia_tree_after_deletion", view=False)
