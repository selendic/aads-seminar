from typing import Optional, Self

import numpy as np


class PrefixTreeNode:
	"""
	A node in a prefix tree.

	Attributes:
		_parent: the parent node
		_children: array of children, indexed by ASCII values
		_num_children: number of non-None children
		_is_final: indicates if the node represents the end of a string
	"""

	@property
	def parent(self):
		return self._parent

	@property
	def num_children(self):
		return self._num_children

	@property
	def is_final(self):
		return self._is_final

	@is_final.setter
	def is_final(self, value: bool):
		self._is_final = value

	def __init__(self, parent: Optional[Self] = None, is_final: bool = False):
		"""
		Initializes a prefix tree node.
		:param parent: the parent node
		"""
		self._parent = parent
		self._children = np.full(256, None)
		self._num_children = 0
		self._is_final = is_final

	def is_leaf(self) -> bool:
		"""
		Check if the node is a leaf.
		:return: True if the node is a leaf, False otherwise
		"""
		return self._num_children == 0

	def transition(self, c: chr) -> Optional[Self]:
		"""
		Transition to the child node corresponding to the character c.
		:param c: character to transition to
		:return: the child node corresponding to the character c if it exists, None otherwise
		"""
		return self._children[ord(c)]

	def insert(self, c: chr) -> Self:
		"""
		Insert a node into the prefix tree.
		:param c: character for the transition
		:return: the child node corresponding to the character c
		"""
		child_node = self.transition(c)
		if child_node is None:
			child_node = PrefixTreeNode(self)
			self._children[ord(c)] = child_node
			self._num_children += 1
		return child_node

	def remove(self, c: chr) -> bool:
		"""
		Remove a node from the prefix tree.
		:param c: character for the transition
		:return: True if the node was removed, False otherwise
		"""
		child_node = self.transition(c)
		if child_node is not None:
			child_node._parent = None
			self._children[ord(c)] = None
			self._num_children -= 1
			return True
		return False


class PrefixTree:
	"""
	A prefix tree.

	Attributes:
		_root: the root node
	"""

	def __init__(self):
		"""
		Initializes a prefix tree.
		"""
		self._root = PrefixTreeNode(None)

	def insert(self, s: str):
		"""
		Insert a string into the prefix tree.
		:param s: string to insert
		"""
		current_node = self._root
		for c in s:
			current_node = current_node.insert(c)
		current_node.is_final = True

	def search(self, q: str) -> Optional[PrefixTreeNode]:
		"""
		Search for a string in the prefix tree.
		:param q: string to search for
		:return: the final node of the string if it exists, None otherwise
		"""
		if self._root is None:
			return None
		current_node = self._root
		for c in q:
			current_node = current_node.transition(c)
			if current_node is None:
				return None
		if current_node.is_final:
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
		end_node.is_final = False
		current_node = end_node
		for c in reversed(s):
			current_node = current_node.parent
			current_node.remove(c)
			if current_node.is_final or not current_node.is_leaf():
				break
		return True
