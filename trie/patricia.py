from typing import Optional, Self

import numpy as np
from graphviz import Digraph


class PatriciaTrieNode:
	"""
	A node in a Patricia trie.

	Attributes:
		s: the string
		p: the starting index of the substring
		l: the length of the substring
		parent: the parent node
		children: array of children, indexed by ASCII values
		num_children: number of non-None children
	"""

	def __init__(self, s: Optional[str], p: int, l: int):
		self.s = s
		self.p = p
		self.l = l
		self.parent = None
		self.children = np.full(256, None)
		self.num_children = 0

	def substring(self) -> str:
		"""
		Get the substring of the node.
		:return: the substring of the node
		"""
		return self.s[self.p: self.p + self.l]

	def is_leaf(self) -> bool:
		"""
		Check if the node is a leaf.
		:return: True if the node is a leaf, False otherwise
		"""
		return self.num_children == 0

	def transition(self, c: chr) -> Optional[Self]:
		"""
		Transition to the child node corresponding to the substring starting with character c.
		:param c: first character of the substring to transition to
		:return: the child node corresponding to the substring starting with character c if it exists, None otherwise
		"""
		return self.children[ord(c)]

	def insert(self, node: Self):
		"""
		Insert a node into the Patricia trie
		:param node: the node to insert
		"""
		if self.children[ord(node.s[node.p])] is None:
			self.num_children += 1
		node.parent = self
		self.children[ord(node.s[node.p])] = node

	def remove(self, node: Self) -> bool:
		"""
		Remove a node from the Patricia trie
		:param node: the node to remove
		:return: True if the node was removed, False otherwise
		"""
		child = self.children[ord(node.s[node.p])]
		if child is not None:
			child.parent = None
			self.num_children -= 1
			self.children[ord(node.s[node.p])] = None
			return True
		return False

	def check_children(self) -> tuple[Optional[Self], bool]:
		"""
		Check how many children does the node have.
		:return: the first child if it exists, and a boolean indicating if it is the only child
		"""
		if self.num_children > 0:
			for child in self.children:
				if child is not None:
					return child, self.num_children == 1
		return None, False


class PatriciaTrie:
	"""
	Initializes a Patricia trie.

	Attributes:
		root: the root node
	"""

	def __init__(self):
		"""
		Initializes a Patricia trie.
		"""
		self.root = PatriciaTrieNode(None, 0, 0)

	def search(self, q: str) -> Optional[PatriciaTrieNode]:
		"""
		Search for a string in the Patricia trie.
		:param q: string to search for
		:return: the node corresponding to the string if it exists, None otherwise
		"""
		q = q + chr(0)
		p, l = 0, len(q)
		current_node = self.root
		while not current_node.is_leaf() and p < l:
			child_node = current_node.transition(q[p])
			if child_node is None:  # not found
				return None
			if q[p: p + child_node.l] != child_node.substring():  # partial match
				return None
			p += child_node.l
			current_node = child_node
		return current_node if p == l else None

	def range_search(self, q: str) -> set[str]:
		"""
		Search for all strings with a given prefix in the Patricia trie.
		:param q: prefix to search for
		:return: list of strings with the given prefix
		"""
		p, l = 0, len(q)
		current_node = self.root
		while not current_node.is_leaf() and p < l:
			child_node = current_node.transition(q[p])
			if child_node is None:  # not found
				return set()
			prefix_len = min(child_node.l, l - p)
			if q[p: p + prefix_len] != child_node.substring()[:prefix_len]:
				return set()
			p += prefix_len
			current_node = child_node
		results = set()
		stack = [current_node]
		while stack:
			current_node = stack.pop()
			if current_node.is_leaf():
				results.add(current_node.s.replace(chr(0), ""))
			else:
				stack.extend([child for child in current_node.children if child is not None])
		return results

	def insert(self, s: str) -> PatriciaTrieNode:
		"""
		Insert a string into the Patricia trie.
		:param s: string to insert
		:return: the final node inserted, which corresponds to the given string
		"""
		s = s + chr(0)
		p, l = 0, len(s)
		current_node = self.root
		while current_node == self.root or not current_node.is_leaf():
			child_node = current_node.transition(s[p])
			if child_node is None:  # insert
				node_to_insert = PatriciaTrieNode(s, p, l - p)
				current_node.insert(node_to_insert)
				return node_to_insert
			if s[p: p + child_node.l] == child_node.substring():  # full match
				p, current_node = p + child_node.l, child_node
				continue
			k = 1
			for i in range(1, child_node.l):  # partial match
				if s[p + i] != child_node.s[child_node.p + i]:
					k = i
					break
			middle_node = PatriciaTrieNode(child_node.s, child_node.p, k)
			child_node.p, child_node.l = child_node.p + k, child_node.l - k
			current_node.insert(middle_node)
			middle_node.insert(child_node)
			end_node = PatriciaTrieNode(s, p + k, l - p - k)
			middle_node.insert(end_node)
			return end_node

	def remove(self, s: str) -> bool:
		"""
		Remove a string from the Patricia trie.
		:param s: string to remove
		:return: True if the string was removed, False otherwise
		"""
		final_node = self.search(s)
		if final_node is None:  # not found
			return False
		current_node = final_node.parent
		if current_node is None:  # final node is root (shouldn't happen theoretically, I guess if None is passed as input string s?)
			return False
		current_node.remove(final_node)
		first_child, is_only_child = current_node.check_children()
		if is_only_child and current_node.parent is not None:
			parent = current_node.parent
			parent.remove(current_node)
			first_child.p -= current_node.l
			first_child.l += current_node.l
			parent.insert(first_child)
		if first_child is not None:
			current_node = first_child
			while current_node.parent is not None:
				if current_node.parent.s == final_node.s:
					current_node.parent.s = current_node.s
				current_node = current_node.parent
		return True

	def visualize(self, file_name: str = "prefix_trie", directory_name: str = "graphviz", view: bool = False):
		"""
		Visualize the Patricia trie using graphviz.
		"""

		def add_nodes(graph: Digraph, node: PatriciaTrieNode, parent_id: str, label: str):
			current_id = str(id(node))
			label = f"{label.replace(chr(0), '¤')}"
			graph.node(current_id, label)
			if parent_id is not None:
				graph.edge(parent_id, current_id)

			for child_node in node.children:
				if child_node is not None:
					assert isinstance(child_node, PatriciaTrieNode)
					add_nodes(graph, child_node, current_id, child_node.substring())

		dot = Digraph(format="png", comment="Patricia Trie")
		dot.attr(dpi="300")
		dot.node(str(id(self.root)), "", shape="diamond", style="filled", fillcolor="black", width="0.1", height="0.1")
		for child in self.root.children:
			if child is not None:
				assert isinstance(child, PatriciaTrieNode)
				add_nodes(dot, child, str(id(self.root)), child.substring())

		dot.render(filename=file_name, directory=directory_name, view=view)
