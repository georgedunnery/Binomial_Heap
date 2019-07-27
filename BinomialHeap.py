# George Dunnery - CS 5800
from Node import *
from math import inf


# Class to represent a binomial heap
class BinomialHeap:

    # Constructs a binomial heap object
    # Initially empty where head is None
    def __init__(self):
        self.head = None

    # Defines the string representation of a binomial heap
    def __str__(self) -> str:
        if self.head is not None:
            return self.head.walk()
        else:
            return ""

    # Function to find the min key in the heap
    # Returns a pointer to the min node
    def min(self) -> 'Node' or None:
        min_node = None
        current = self.head
        # Initialize the minimum value as negative infinity
        min_val = inf
        while current is not None:
            if current.key < min_val:
                min_val = current.key
                min_node = current
            # Traverse root list, since the min must be a root (all node keys larger)
            current = current.sibling
        return min_node

    # Function to link two binomial trees by manipulating the roots
    #  new_child: Node, the root of the tree to link under a different root
    #  root: Node, the root to which the new_child will be linked (becomes parent)
    # Returns nothing
    def tree_link(self, new_child: 'Node', root: 'Node') -> None:
        # Prevent property violation (root key < all child keys)
        if root.key > new_child.key:
            raise ValueError("Child keys must be larger than parent keys.")
        # Prevent breaking pointer references and NoneType error
        if new_child is None or root is None:
            raise ValueError("Node(s) cannot be None for link operation.")
        new_child.parent = root
        new_child.sibling = root.child
        root.child = new_child
        root.degree += 1

    # Auxiliary function to union, please use union instead!
    # Function to merge two binomial heaps into one
    # Adds binomial trees in degree order
    #  other_heap: BinomialHeap, heap to merge with the current heap
    # Returns Node, the head of the root list for a new BinomialHeap
    def heap_merge(self, other_heap: 'BinomialHeap') -> 'Node' or None:
        # Assume: at most 1 tree per degree per heap, and already in order by degree
        # Start at the heads, add the lesser degree tree until both root lists exhausted
        # Refer to self as x, other as y
        x_node = self.head
        y_node = other_heap.head
        # Node selected to insert
        selected = None
        # The head of root list (returned value)
        head_node = None
        # Reference to the previous node (reverse sibling)
        prev_node = None
        # While there are still binomial trees to add
        while x_node is not None or y_node is not None:
            # Step 1: Select the root list node that should come next
            # When x is none, add the rest of y
            if x_node is None:
                selected = y_node
                y_node = y_node.sibling
            # When y is none, add the rest of x
            elif y_node is None:
                selected = x_node
                x_node = x_node.sibling
            # Root x has smaller degree tree
            elif x_node.degree <= y_node.degree:
                selected = x_node
                x_node = x_node.sibling
            # Root y has smaller degree tree
            else:
                selected = y_node
                y_node = y_node.sibling
            # Step 2: Record the selection
            # Set the head node (first iteration only)
            if head_node is None:
                head_node = selected
            # Set the sibling of the previous node to the current node
            else:
                prev_node.sibling = selected
            # Always maintain reference to previous node
            prev_node = selected
        # Return pointer to head of root list (binomial trees may need linking)
        return head_node

    # Function to generate heap from union of two binomial heaps (current and other)
    #  other_heap: the other heap to merge with the current heap
    # Returns BinomialHeap, the result of the union
    def union(self, other_heap) -> 'BinomialHeap':
        # Create new heap and set head as returned node from merging
        unite = BinomialHeap()
        unite.head = self.heap_merge(other_heap)
        if unite.head is None:
            return unite
        # Fix the list by linking duplicate degree trees
        prev = None
        current = unite.head
        nxt = current.sibling
        while nxt is not None:
            if (current.degree != nxt.degree or
                    nxt.sibling is not None and nxt.sibling.degree == current.degree):
                prev = current
                current = nxt
            else:
                if current.key <= nxt.key:
                    current.sibling = nxt.sibling
                    self.tree_link(nxt, current)
                else:
                    if prev is None:
                        unite.head = nxt
                    else:
                        prev.sibling = nxt
                    self.tree_link(current, nxt)
                    current = nxt
            nxt = current.sibling
        return unite

    # Function to insert a node into the binomial heap
    #  node: Node, the node to add to the binomial heap
    # Returns nothing
    def insert(self, node: 'Node') -> None:
        # Method: Create a heap with just one node, then merge the heaps
        # and reassign the head node of the root list in the calling heap
        singleton = BinomialHeap()
        # Restore default attributes of the node
        node.parent = None
        node.child = None
        node.sibling = None
        node.degree = 0
        # Assign as the head of the other heap, then merge
        singleton.head = node
        self.head = self.union(singleton).head

    # Function to remove and return the node with the minimum key
    # Returns Node, the node with the minimum key
    def extract_min(self) -> 'Node':
        if self.head is None:
            raise Exception("Heap is empty.")
        # Step 1: Find the minimum node in the heap (in root list)
        # Maintain reference to the preceding node to min_node
        prev = None
        min_node = None
        # Traverse root list at current with prev reference in left_sibling
        current = self.head
        left_sibling = None
        # Initialize the minimum value as negative infinity
        min_val = inf
        while current is not None:
            if current.key < min_val:
                min_val = current.key
                min_node = current
                # Track the preceding node to the minimum
                prev = left_sibling
            left_sibling = current
            current = current.sibling
        # Step 2: Remove the min_node and process its children
        # Splice out the node by reassigning pointer past min_node
        # When prev is None, min_node was head
        if prev is None:
            self.head = min_node.sibling
        else:
            prev.sibling = min_node.sibling
        # Create an auxiliary heap to process the children nodes
        heap = BinomialHeap()
        # Reverse the order of the the children nodes (prepend)
        node = min_node.child
        while node is not None:
            # Keep reference to the next child
            nxt = node.sibling
            # Remove parent reference (the node to be extracted)
            node.parent = None
            # Prepend: set old head as sibling and node as new head
            node.sibling = heap.head
            heap.head = node
            # Move on to the next child using nxt reference
            node = nxt
        # Step 3: Merge the heaps and return the minimum node
        self.head = self.union(heap).head
        return min_node

    # Function to decrease the key of a node to a new value
    #  node: Node, the node that will have its key decreased
    #  new_key: integer or float, the new key for the node (must be smaller)
    # Returns nothing
    def decrease_key(self, node: 'Node', new_key: int or float) -> None:
        # Throw an exception if the new key is larger than the old key
        if new_key > node.key:
            raise ValueError("The new key must be less than or equal to the old key.")
        node.key = new_key
        # Bubble up, fixing the heap property if needed (parent <= child)
        current = node
        above = current.parent
        while above is not None and current.key < above.key:
            # Exchange keys
            tmp = current.key
            current.key = above.key
            above.key = tmp
            # Sibling & child attributes are already correct after exchange keys
            # Shift up
            current = above
            above = above.parent

    # Function to delete a node
    #  node: Node, the node to delete from the binomial heap
    # Returns nothing
    def delete(self, node: 'Node') -> None:
        # Force node to min by setting key = -infinity
        self.decrease_key(node, -inf)
        # Extract min will remove it, ignore the returned node
        self.extract_min()
