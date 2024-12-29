from typing import Optional, Self

import numpy as np
from graphviz import Digraph


class PrefixTreeNode:
	"""
	A node in a prefix tree.

	Attributes:
		parent: the parent node
		children: array of children, indexed by ASCII values
		num_children: number of non-None children
	"""

	def __init__(self, parent: Optional[Self] = None):
		"""
		Initializes a prefix tree node.
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
		Insert a node into the prefix tree.
		:param c: character for the transition
		:return: the child node corresponding to the character c
		"""
		child_node = self.transition(c)
		if child_node is None:
			child_node = PrefixTreeNode(self)
			self.children[ord(c)] = child_node
			self.num_children += 1
		return child_node

	def remove(self, c: chr) -> bool:
		"""
		Remove a node from the prefix tree.
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


class PrefixTree:
	"""
	A prefix tree.

	Attributes:
		root: the root node
	"""

	def __init__(self):
		"""
		Initializes a prefix tree.
		"""
		self.root = PrefixTreeNode(None)

	def insert(self, s: str):
		"""
		Insert a string into the prefix tree.
		:param s: string to insert
		"""
		current_node = self.root
		for c in s + chr(0):
			current_node = current_node.insert(c)

	def search(self, q: str) -> Optional[PrefixTreeNode]:
		"""
		Search for a string in the prefix tree.
		:param q: string to search for
		:return: the final node of the string if it exists, None otherwise
		"""
		if self.root is None:
			return None
		current_node = self.root
		for c in q + chr(0):
			current_node = current_node.transition(c)
			if current_node is None:
				return None
		return current_node

	def remove(self, s: str) -> bool:
		"""
		Remove a string from the prefix tree.
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

	def visualize(self, file_name: str = "prefix_tree", directory_name: str = "graphviz", view: bool = False):
		"""
		Visualize the prefix tree using graphviz.
		"""

		def add_nodes(graph: Digraph, node: PrefixTreeNode, parent_id: str, char: chr):
			current_id = str(id(node))
			label = '¤' if char == chr(0) else char
			graph.node(current_id, label)
			if parent_id is not None:
				graph.edge(parent_id, current_id)

			for j, child_node in enumerate(node.children):
				if child_node is not None:
					assert isinstance(child_node, PrefixTreeNode)
					add_nodes(graph, child_node, current_id, chr(j))

		dot = Digraph(format="png", comment="Prefix Tree")
		dot.attr(dpi="300")
		dot.node(str(id(self.root)), "ROOT")
		for i, child in enumerate(self.root.children):
			if child is not None:
				assert isinstance(child, PrefixTreeNode)
				add_nodes(dot, child, str(id(self.root)), chr(i))

		dot.render(filename=file_name, directory=directory_name, view=view)
