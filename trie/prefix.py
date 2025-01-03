from typing import Optional, Self

import numpy as np
from graphviz import Digraph


class PrefixTrieNode:
	"""
	A node in a prefix trie.

	Attributes:
		parent: the parent node
		children: array of children, indexed by ASCII values
		num_children: number of non-None children
	"""

	def __init__(self, parent: Optional[Self] = None):
		"""
		Initializes a prefix trie node.
		:param parent: the parent node
		"""
		self.parent = parent
		self.children = np.full(256, None, dtype=object)
		self.num_children = 0

	def is_leaf(self) -> bool:
		"""
		Check if the node is a leaf.
		:return: True if the node is a leaf, False otherwise
		"""
		return self.num_children == 0

	def transition(self, c: chr) -> Optional[Self]:
		"""
		Transition to the child node corresponding to the character c.
		:param c: character to transition to
		:return: the child node corresponding to the character c if it exists, None otherwise
		"""
		return self.children[ord(c)]

	def insert(self, c: chr) -> Self:
		"""
		Insert a node into the prefix trie.
		:param c: character for the transition
		:return: the inserted node
		"""
		child_node = self.transition(c)
		if child_node is None:
			child_node = PrefixTrieNode(self)
			self.children[ord(c)] = child_node
			self.num_children += 1
		return child_node

	def remove(self, c: chr) -> bool:
		"""
		Remove a node from the prefix trie.
		:param c: character for the transition
		:return: True if the node was removed, False otherwise
		"""
		child_node = self.transition(c)
		if child_node is not None:
			child_node.parent = None
			self.children[ord(c)] = None
			self.num_children -= 1
			return True
		return False


class PrefixTrie:
	"""
	A prefix trie.

	Attributes:
		root: the root node
	"""

	def __init__(self):
		"""
		Initializes a prefix trie.
		"""
		self.root = PrefixTrieNode(None)

	def _search(self, prefix: str) -> Optional[PrefixTrieNode]:
		"""
		Search for a prefix in the prefix trie.
		:param prefix: prefix to search for
		:return: the final node of the prefix if it exists, None otherwise
		"""
		if self.root is None:
			return None
		current_node = self.root
		for c in prefix:
			current_node = current_node.transition(c)
			if current_node is None:
				return None
		return current_node

	def search(self, q: str) -> Optional[PrefixTrieNode]:
		"""
		Search for a string in the prefix trie.
		:param q: string to search for
		:return: the final node of the string if it exists, None otherwise
		"""
		return self._search(q + chr(0))

	def range_search(self, q: str) -> set[str]:
		"""
		Search for all strings with a given prefix in the prefix trie.
		:param q: prefix to search for
		:return: list of strings with the given prefix
		"""
		current_node = self._search(q)
		if current_node is None:
			return set()
		words = set()
		stack = [(q, current_node)]
		while stack:
			current_prefix, current_node = stack.pop()
			for j, child_node in enumerate(current_node.children):
				if child_node is not None:
					if chr(j) == chr(0):
						words.add(current_prefix)
					else:
						stack.append((current_prefix + chr(j), child_node))
		return words

	def insert(self, s: str):
		"""
		Insert a string into the prefix trie.
		:param s: string to insert
		"""
		current_node = self.root
		for c in s + chr(0):
			current_node = current_node.insert(c)

	def remove(self, s: str) -> bool:
		"""
		Remove a string from the prefix trie.
		:param s: string to remove
		:return: True if the string was removed, False otherwise
		"""
		# Firstly, find the end node of the string
		end_node = self.search(s)
		if end_node is None:
			return False
		# Then, remove the nodes one by one in reverse order
		current_node = end_node
		for c in reversed(s + chr(0)):
			if not current_node.is_leaf():
				break
			current_node = current_node.parent
			current_node.remove(c)

	def visualize(self, file_name: str = "prefix_trie", directory_name: str = "graphviz", view: bool = False):
		"""
		Visualize the prefix trie using graphviz.
		"""

		def add_nodes(graph: Digraph, node: PrefixTrieNode, parent_id: str, char: chr):
			current_id = str(id(node))
			label = '¤' if char == chr(0) else char
			graph.node(current_id, label)
			if parent_id is not None:
				graph.edge(parent_id, current_id)

			for j, child_node in enumerate(node.children):
				if child_node is not None:
					assert isinstance(child_node, PrefixTrieNode)
					add_nodes(graph, child_node, current_id, chr(j))

		dot = Digraph(format="png", comment="Prefix Trie")
		dot.attr(dpi="300")
		dot.node(str(id(self.root)), "", shape="diamond", style="filled", fillcolor="black", width="0.2", height="0.2")
		for i, child in enumerate(self.root.children):
			if child is not None:
				assert isinstance(child, PrefixTrieNode)
				add_nodes(dot, child, str(id(self.root)), chr(i))

		dot.render(filename=file_name, directory=directory_name, view=view)
