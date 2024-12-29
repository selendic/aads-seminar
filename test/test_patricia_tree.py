import os
import unittest

from src.patricia_tree import PatriciaTree, PatriciaTreeNode


class TestPatriciaTree(unittest.TestCase):

	def setUp(self):
		"""Set up a new PatriciaTree for each test."""
		self.tree = PatriciaTree()

	def test_insert_and_search(self):
		"""Test inserting and searching for strings."""
		self.tree.insert("hello")
		self.tree.insert("world")
		self.tree.insert("help")

		# Search for exact strings
		self.assertIsNotNone(self.tree.search("hello"))
		self.assertIsNotNone(self.tree.search("world"))
		self.assertIsNotNone(self.tree.search("help"))

		# Search for prefixes (should not match unless exact)
		self.assertIsNone(self.tree.search("hel"))
		self.assertIsNone(self.tree.search("worl"))

		# Search for a string not in the tree
		self.assertIsNone(self.tree.search("notinthetree"))

	def test_remove(self):
		"""Test removing strings from the Patricia tree."""
		self.tree.insert("hello")
		self.tree.insert("help")

		# Verify strings exist before removal
		self.assertIsNotNone(self.tree.search("hello"))
		self.assertIsNotNone(self.tree.search("help"))

		# Remove one string and verify the other still exists
		self.tree.remove("hello")
		self.assertIsNone(self.tree.search("hello"))
		self.assertIsNotNone(self.tree.search("help"))

		# Remove the other string
		self.tree.remove("help")
		self.assertIsNone(self.tree.search("help"))

		# Attempt to remove a string not in the tree
		self.assertFalse(self.tree.remove("nonexistent"))

	def test_empty_string(self):
		"""Test handling of empty strings."""
		self.tree.insert("")
		self.assertIsNotNone(self.tree.search(""))
		self.tree.remove("")
		self.assertIsNone(self.tree.search(""))

	def test_common_prefixes(self):
		"""Test inserting strings with common prefixes."""
		self.tree.insert("prefix")
		self.tree.insert("prefecture")
		self.tree.insert("pref")

		# Verify all strings exist
		self.assertIsNotNone(self.tree.search("prefix"))
		self.assertIsNotNone(self.tree.search("prefecture"))
		self.assertIsNotNone(self.tree.search("pref"))

		# Verify removing one does not affect others
		self.tree.remove("prefix")
		self.assertIsNone(self.tree.search("prefix"))
		self.assertIsNotNone(self.tree.search("prefecture"))
		self.assertIsNotNone(self.tree.search("pref"))

	def test_is_leaf(self):
		"""Test the is_leaf method of PatriciaTreeNode."""
		root = self.tree.root
		self.assertTrue(root.is_leaf())  # Root is initially a leaf

		# Add a child and check again
		child = PatriciaTreeNode("test", 0, 1)
		root.insert(child)
		self.assertFalse(root.is_leaf())
		self.assertTrue(child.is_leaf())

	def test_visualize(self):
		"""Test that visualize runs without errors."""
		self.tree.insert("test")
		self.tree.insert("testing")
		self.tree.insert("tester")

		try:
			self.tree.visualize(file_name="test_patricia_tree", directory_name=".", view=False)
		except Exception as e:
			self.fail(f"Visualization failed with exception: {e}")
		finally:
			os.remove("test_patricia_tree")
			os.remove("test_patricia_tree.png")

if __name__ == "__main__":
	unittest.main()
