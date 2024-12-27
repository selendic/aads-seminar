from typing import Self

import numpy as np


class PatriciaTreeNode:
	s: str | None  # pointer to full string, None if root or leaf
	p: int  # pointer to first character in the represented substring
	l: int  # length of the represented substring
	children: np.array  # array of children, sigma = ascii
	num_children: int  # number of non-None children
	parent: object  # parent node

	def __init__(self, s: str | None, p: int, l: int):
		self.s = s
		self.p = p
		self.l = l
		self.children = np.array([None]) * 256
		self.num_children = 0
		self.parent = None

	def is_leaf(self) -> bool:
		return self.num_children == 0

	def transition(self, c: chr) -> Self:
		return self.children[ord(c)]

	def insert(self, cnc: Self):
		if self.children[ord(cnc.s[cnc.p])] is None:
			self.num_children += 1
			cnc.parent = self
			self.children[ord(cnc.s[cnc.p])] = cnc

	def remove(self, cnc: Self):
		child = self.children[ord(cnc.s[cnc.p])]
		if child is not None:
			child.parent = None
			self.num_children -= 1
			self.children[ord(cnc.s[cnc.p])] = None

	def check_children(self):
		if self.num_children > 0:
			for child in self.children:
				if child is not None:
					return self.num_children == 1, child
		return False, None


class PatriciaTree:
	root: PatriciaTreeNode

	def __init__(self):
		self.root = PatriciaTreeNode(None, 0, 0)

	def search(self, q: str) -> bool:
		succ, cn = self._search(q)
		return succ

	def _search(self, q: str) -> (bool, PatriciaTreeNode):
		q = q + '$'
		q_p, q_l = 0, len(q)
		sc = 0
		cn = self.root
		while not cn.is_leaf():
			cnc = cn.transition(q[sc])
			if cnc is None:
				return False, None
			t_p, t_l = cnc.p, cnc.l
			if q[sc: sc + t_l] != cnc.s[t_p: t_p + t_l]:
				return False, None
			sc, cn = sc + t_l, cnc
		return sc == q_l, cn
