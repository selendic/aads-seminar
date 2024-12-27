from typing import Self

class PLString:
	def __init__(self, s: str, p: int, l: int):
		if p < 0 or p >= len(s):
			raise ValueError("0 <= p < len(s) must hold")
		if l <= 0 or p + l > len(s):
			raise ValueError("0 < l <= len(s) - p must hold")
		self.s = s
		self.p = p
		self.l = l
	def get(self) -> str:
		return self.s[self.p: self.p + self.l]
	def clone(self) -> Self:
		return PLString(self.s, self.p, self.l)