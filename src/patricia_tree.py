from typing import Optional, Self

import numpy as np
from graphviz import Digraph


class PatriciaTreeNode:
	def __init__(self, s: Optional[str], p: int, l: int):
		self.s = s
		self.p = p
		self.l = l
		self.children = np.full(256, None)
		self.num_children = 0
		self.parent = None

	def substring(self) -> str:
		return self.s[self.p: self.p + self.l]

	def is_leaf(self) -> bool:
		return self.num_children == 0

	def transition(self, c: chr) -> Self:
		return self.children[ord(c)]

	def insert(self, node: Self):
		if self.children[ord(node.s[node.p])] is None:
			self.num_children += 1
		node.parent = self
		self.children[ord(node.s[node.p])] = node

	def remove(self, node: Self):
		child = self.children[ord(node.s[node.p])]
		if child is not None:
			child.parent = None
			self.num_children -= 1
			self.children[ord(node.s[node.p])] = None

	def check_children(self) -> tuple[Optional[Self], bool]:
		if self.num_children > 0:
			for child in self.children:
				if child is not None:
					return child, self.num_children == 1
		return None, False


class PatriciaTree:
	"""
	Initializes a Patricia tree.
	"""

	def __init__(self):
		self.root = PatriciaTreeNode(None, 0, 0)

	def search(self, q: str) -> Optional[PatriciaTreeNode]:
		q = q + chr(0)
		p, l = 0, len(q)
		current_node = self.root
		while not current_node.is_leaf():
			child_node = current_node.transition(q[p])
			if child_node is None:
				return None
			if q[p: p + child_node.l] != child_node.substring():
				return None
			p, current_node = p + child_node.l, child_node
		return current_node if p == l else None

	def insert(self, s: str) -> PatriciaTreeNode:
		s = s + chr(0)
		p, l = 0, len(s)
		current_node = self.root
		while current_node == self.root or not current_node.is_leaf():
			child_node = current_node.transition(s[p])
			if child_node is None:  # insert
				node_to_insert = PatriciaTreeNode(s, p, l - p)
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
			middle_node = PatriciaTreeNode(child_node.s, child_node.p, k)
			child_node.p, child_node.l = child_node.p + k, child_node.l - k
			current_node.insert(middle_node)
			middle_node.insert(child_node)
			end_node = PatriciaTreeNode(s, p + k, l - p - k)
			middle_node.insert(end_node)
			return end_node

	def remove(self, s: str) -> bool:
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

	def visualize(self, file_name: str = "prefix_tree", directory_name: str = "graphviz", view: bool = False):
		"""
		Visualize the Patricia tree using graphviz.
		"""

		def add_nodes(graph: Digraph, node: PatriciaTreeNode, parent_id: str, label: str):
			current_id = str(id(node))
			label = f"{label.replace(chr(0), '¤')}"
			graph.node(current_id, label)
			if parent_id is not None:
				graph.edge(parent_id, current_id)

			for child_node in node.children:
				if child_node is not None:
					assert isinstance(child_node, PatriciaTreeNode)
					add_nodes(graph, child_node, current_id, child_node.substring())

		dot = Digraph(format="png", comment="Patricia Tree")
		dot.attr(dpi="300")
		dot.node(str(id(self.root)), "ROOT")
		for child in self.root.children:
			if child is not None:
				assert isinstance(child, PatriciaTreeNode)
				add_nodes(dot, child, str(id(self.root)), child.substring())

		dot.render(filename=file_name, directory=directory_name, view=view)
