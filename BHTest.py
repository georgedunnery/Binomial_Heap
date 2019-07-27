# George Dunnery - CS 5800
from BinomialHeap import *
import unittest


# Test class focusing on node functionality
class NodeTest(unittest.TestCase):

    # Verify that integer keys are enforced
    def test_create_node_exception(self):
        try:
            incorrect = Node("hello")
        except TypeError:
            # Verify that the exception is thrown as expected
            pass

    # Verify that a node is created correctly
    def test_create_node(self):
        test_node = Node(1)
        self.assertEqual(1, test_node.key)
        self.assertEqual(0, test_node.degree)
        self.assertIsNone(test_node.parent)
        self.assertIsNone(test_node.child)
        self.assertIsNone(test_node.sibling)
        test_node = Node(2743562)
        self.assertEqual(2743562, test_node.key)
        test_node = Node(-99281)
        self.assertEqual(-99281, test_node.key)
        # -inf will be the key prior to deletion
        test_node = Node(float(-inf))
        self.assertEqual(-inf, test_node.key)


# Test class focusing on binomial heap functionality
class BinomialHeapTest(unittest.TestCase):

    # Verify binomial heap initialization
    def test_create_heap(self):
        heap = BinomialHeap()
        self.assertIsNone(heap.head)

    # Verify the minimum key is found
    def test_heap_min(self):
        # Manually insert root list for this test
        # Check address & key value
        heap = BinomialHeap()
        first = Node(150)
        heap.head = first
        # Only one node in the root list
        self.assertEqual(first, heap.min())
        self.assertEqual(150, heap.min().key)
        # Min is later in the list
        second = Node(97)
        heap.head.sibling = second
        self.assertEqual(second, heap.min())
        self.assertEqual(97, heap.min().key)
        # Min is in the middle
        third = Node(500)
        heap.head.sibling.sibling = third
        self.assertEqual(second, heap.min())
        self.assertEqual(97, heap.min().key)
        # Min is negative
        fourth = Node(-1)
        heap.head.sibling.sibling.sibling = fourth
        self.assertEqual(fourth, heap.min())
        self.assertEqual(-1, heap.min().key)

    # Verify the linking functions properly
    def test_tree_link(self):
        # First binomial tree
        root = Node(2)
        root.child = Node(5)
        root.degree += 1
        # Other binomial tree
        new_child = Node(4)
        new_child.child = Node(6)
        new_child.degree += 1
        # Heap with root list [2, 4]
        heap = BinomialHeap()
        heap.head = root
        root.sibling = new_child
        # Link new_child underneath root
        heap.tree_link(new_child, root)
        # Check degree incremented
        self.assertEqual(2, heap.head.degree)
        self.assertEqual(2, root.degree)
        # Check child is now new_child
        self.assertEqual(new_child, heap.head.child)
        # Check child's sibling is the old child and next sibling still None
        self.assertEqual(5, heap.head.child.sibling.key)
        self.assertIsNone(heap.head.child.sibling.sibling)
        # Check new child's child
        self.assertEqual(6, heap.head.child.child.key)
        # Must manually remove reference to new_child in the root nodes list!
        heap.head.sibling = None
        self.assertIsNone(heap.head.sibling)

    # Verify the heap merge functions correctly
    # Manually set node attributes since insert runs on union, which runs on heap_merge
    def test_heap_merge(self):
        # Create & verify the first heap
        heap = BinomialHeap()
        expected = ""
        self.assertEqual(expected, str(heap))
        a = Node(5)
        heap.head = a
        expected = "(k=5, p=None, d=0)"
        self.assertEqual(expected, str(heap))
        b = Node(10)
        c = Node(20)
        a.sibling = b
        b.child = c
        b.degree += 1
        c.parent = b
        expected = "(k=5, p=None, d=0)" \
                   "(k=10, p=None, d=1)(k=20, p=10, d=0)"
        self.assertEqual(expected, str(heap))
        # Create & verify the second heap
        other = BinomialHeap()
        d = Node(3)
        other.head = d
        expected = "(k=3, p=None, d=0)"
        self.assertEqual(expected, str(other))
        e = Node(12)
        d.sibling = e
        f = Node(18)
        e.child = f
        e.degree += 1
        f.parent = e
        expected = "(k=3, p=None, d=0)" \
                   "(k=12, p=None, d=1)(k=18, p=12, d=0)"
        self.assertEqual(expected, str(other))
        g = Node(39)
        e.sibling = g
        h = Node(59)
        g.degree += 1
        g.child = h
        h.parent = g
        i = Node(60)
        i.sibling = g.child
        i.parent = g
        g.degree += 1
        g.child = i
        j = Node(150)
        i.child = j
        i.degree += 1
        j.parent = i
        expected = "(k=3, p=None, d=0)" \
                   "(k=12, p=None, d=1)(k=18, p=12, d=0)" \
                   "(k=39, p=None, d=2)(k=60, p=39, d=1)(k=150, p=60, d=0)(k=59, p=39, d=0)"
        self.assertEqual(expected, str(other))
        # Merge the heaps and validate the results (in order of root list node's degree)
        heap.heap_merge(other)
        expected = "(k=5, p=None, d=0)" \
                   "(k=3, p=None, d=0)" \
                   "(k=10, p=None, d=1)(k=20, p=10, d=0)" \
                   "(k=12, p=None, d=1)(k=18, p=12, d=0)" \
                   "(k=39, p=None, d=2)(k=60, p=39, d=1)(k=150, p=60, d=0)(k=59, p=39, d=0)"
        self.assertEqual(expected, str(heap))

    # Verify that union functions correctly
    # The same test case from test_heap_merge above is used again
    def test_union(self):
        # Create & verify the first heap
        heap = BinomialHeap()
        expected = ""
        self.assertEqual(expected, str(heap))
        a = Node(5)
        heap.head = a
        expected = "(k=5, p=None, d=0)"
        self.assertEqual(expected, str(heap))
        b = Node(10)
        c = Node(20)
        a.sibling = b
        b.child = c
        b.degree += 1
        c.parent = b
        expected = "(k=5, p=None, d=0)" \
                   "(k=10, p=None, d=1)(k=20, p=10, d=0)"
        self.assertEqual(expected, str(heap))
        # Create & verify the second heap
        other = BinomialHeap()
        d = Node(3)
        other.head = d
        expected = "(k=3, p=None, d=0)"
        self.assertEqual(expected, str(other))
        e = Node(12)
        d.sibling = e
        f = Node(18)
        e.child = f
        e.degree += 1
        f.parent = e
        expected = "(k=3, p=None, d=0)" \
                   "(k=12, p=None, d=1)(k=18, p=12, d=0)"
        self.assertEqual(expected, str(other))
        g = Node(39)
        e.sibling = g
        h = Node(59)
        g.degree += 1
        g.child = h
        h.parent = g
        i = Node(60)
        i.sibling = g.child
        i.parent = g
        g.degree += 1
        g.child = i
        j = Node(150)
        i.child = j
        i.degree += 1
        j.parent = i
        expected = "(k=3, p=None, d=0)" \
                   "(k=12, p=None, d=1)(k=18, p=12, d=0)" \
                   "(k=39, p=None, d=2)(k=60, p=39, d=1)(k=150, p=60, d=0)(k=59, p=39, d=0)"
        self.assertEqual(expected, str(other))
        # Perform a union between the heaps and validate the results
        heap = heap.union(other)
        expected = "(k=3, p=None, d=1)(k=5, p=3, d=0)" \
                   "(k=10, p=None, d=3)(k=39, p=10, d=2)(k=60, p=39, d=1)(k=150, p=60, d=0)" \
                   "(k=59, p=39, d=0)(k=12, p=10, d=1)(k=18, p=12, d=0)(k=20, p=10, d=0)"
        self.assertEqual(expected, str(other))

    # Verify nodes are inserted properly
    def test_insert(self):
        heap = BinomialHeap()
        a = Node(5)
        # Inserting the head node
        heap.insert(a)
        self.assertEqual(a, heap.head)
        self.assertEqual(5, heap.head.key)
        self.assertEqual(0, heap.head.degree)
        expected = "(k=5, p=None, d=0)"
        self.assertEqual(expected, str(heap))
        # Smaller node of same degree, new parent and root list head
        b = Node(4)
        heap.insert(b)
        self.assertEqual(b, heap.head)
        self.assertEqual(a, b.child)
        self.assertEqual(b, a.parent)
        expected = "(k=4, p=None, d=1)(k=5, p=4, d=0)"
        self.assertEqual(expected, str(heap))
        # New node is larger, but smallest degree should be new head
        c = Node(25)
        heap.insert(c)
        self.assertEqual(c, heap.head)
        self.assertEqual(b, c.sibling)
        expected = "(k=25, p=None, d=0)" \
                   "(k=4, p=None, d=1)(k=5, p=4, d=0)"
        self.assertEqual(expected, str(heap))
        # New smallest node will become head & have degree 2
        d = Node(-13)
        heap.insert(d)
        self.assertEqual(d, heap.head)
        self.assertIsNone(d.sibling)
        self.assertEqual(d, b.parent)
        self.assertEqual(d, c.parent)
        self.assertEqual(2, d.degree)
        expected = "(k=-13, p=None, d=2)" \
                   "(k=4, p=-13, d=1)(k=5, p=4, d=0)" \
                   "(k=25, p=-13, d=0)"
        self.assertEqual(expected, str(heap))

    # Verify extract_min works as expected
    def test_extract_min(self):
        heap = BinomialHeap()
        # Single node, removed after extract min
        a = Node(10)
        heap.insert(a)
        expected = "(k=10, p=None, d=0)"
        self.assertEqual(expected, str(heap))
        node = heap.extract_min()
        self.assertEqual("", str(heap))
        self.assertEqual(a, node)
        # Two nodes: degree change, child becomes head
        a = Node(7)
        b = Node(5)
        heap.insert(a)
        heap.insert(b)
        expected = "(k=5, p=None, d=1)(k=7, p=5, d=0)"
        self.assertEqual(expected, str(heap))
        node = heap.extract_min()
        expected = "(k=7, p=None, d=0)"
        self.assertEqual(expected, str(heap))
        self.assertEqual(b, node)
        # Insert many nodes to create complexity
        c = Node(20)
        d = Node(30)
        e = Node(25)
        f = Node(13)
        g = Node(14)
        h = Node(-1)
        i = Node(9)
        j = Node(11)
        heap.insert(b)
        heap.insert(c)
        heap.insert(d)
        heap.insert(e)
        heap.insert(f)
        heap.insert(g)
        heap.insert(h)
        heap.insert(i)
        heap.insert(j)
        expected = "(k=9, p=None, d=1)(k=11, p=9, d=0)" \
                   "(k=-1, p=None, d=3)" \
                   "(k=5, p=-1, d=2)(k=20, p=5, d=1)(k=30, p=20, d=0)(k=7, p=5, d=0)" \
                   "(k=13, p=-1, d=1)(k=25, p=13, d=0)" \
                   "(k=14, p=-1, d=0)"
        self.assertEqual(expected, str(heap))
        # Extract -1, a lot of rearrangement necessary
        node = heap.extract_min()
        self.assertEqual(h, node)
        expected = "(k=14, p=None, d=0)" \
                   "(k=5, p=None, d=3)" \
                   "(k=9, p=5, d=2)(k=13, p=9, d=1)(k=25, p=13, d=0)(k=11, p=9, d=0)" \
                   "(k=20, p=5, d=1)(k=30, p=20, d=0)" \
                   "(k=7, p=5, d=0)"
        self.assertEqual(expected, str(heap))

    # Verify key changes to lower value & structure updates as needed
    # Note: Keys are swapped, not the node objects themselves (address)
    # Check where the new smaller key should bubble up to
    def test_decrease_key(self):
        heap = BinomialHeap()
        heap.insert(Node(100))
        self.assertEqual(100, heap.head.key)
        heap.decrease_key(heap.head, 99)
        self.assertEqual(99, heap.head.key)
        heap.insert(Node(55))
        self.assertEqual(55, heap.head.key)
        heap.decrease_key(heap.head.child, 21)
        self.assertEqual(21, heap.head.key)
        heap.insert(Node(15))
        heap.insert(Node(14))
        expected = "(k=14, p=None, d=2)" \
                   "(k=21, p=14, d=1)(k=55, p=21, d=0)" \
                   "(k=15, p=14, d=0)"
        self.assertEqual(expected, str(heap))
        # Change 55 (bottom) to 13
        # 21 should take its place, and 13 should bubble to the root
        self.assertEqual(55, heap.head.child.child.key)
        heap.decrease_key(heap.head.child.child, 13)
        self.assertEqual(21, heap.head.child.child.key)
        self.assertEqual(13, heap.head.key)
        expected = "(k=13, p=None, d=2)" \
                   "(k=14, p=13, d=1)(k=21, p=14, d=0)" \
                   "(k=15, p=13, d=0)"
        self.assertEqual(expected, str(heap))
        # Attempt to increase key back to 55 (expect error)
        try:
            heap.decrease_key(heap.head, 14)
        except ValueError:
            # Error was thrown appropriately
            pass

    # Verify that deletions are handled properly
    # Relies on decrease_key and extract_min!
    def test_delete(self):
        heap = BinomialHeap()
        a = Node(9)
        heap.insert(a)
        expected = "(k=9, p=None, d=0)"
        self.assertEqual(expected, str(heap))
        heap.delete(a)
        self.assertEqual("", str(heap))
        a = Node(8)
        b = Node(10)
        c = Node(-3)
        d = Node(4)
        e = Node(7)
        heap.insert(a)
        heap.insert(b)
        heap.insert(c)
        heap.insert(d)
        heap.insert(e)
        expected = "(k=7, p=None, d=0)" \
                   "(k=-3, p=None, d=2)(k=8, p=-3, d=1)(k=10, p=8, d=0)" \
                   "(k=4, p=-3, d=0)"
        self.assertEqual(expected, str(heap))
        heap.delete(e)
        expected = "(k=-3, p=None, d=2)(k=8, p=-3, d=1)(k=10, p=8, d=0)(k=4, p=-3, d=0)"
        self.assertEqual(expected, str(heap))
        heap.delete(c)
        expected = "(k=4, p=None, d=0)(k=8, p=None, d=1)(k=10, p=8, d=0)"
        self.assertEqual(expected, str(heap))
        heap.delete(a)
        expected = "(k=4, p=None, d=1)(k=10, p=4, d=0)"
        self.assertEqual(expected, str(heap))
        heap.delete(d)
        expected = "(k=10, p=None, d=0)"
        self.assertEqual(expected, str(heap))
        heap.delete(b)
        self.assertEqual("", str(heap))


def main():
    unittest.main(verbosity=3)


main()
