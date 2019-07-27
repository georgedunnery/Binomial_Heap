# George Dunnery - CS 5800


# Class to represent a node in a binomial heap
class Node:

    # Constructs a node object
    #  key: integer or float, the value of the node
    # Note - float required to store negative infinity during deletion
    def __init__(self, key: int or float):
        # Enforce integer keys
        if type(key) != int and type(key) != float:
            raise TypeError("Key must be an integer or float.")
        self.key = key
        # Degree is the number of child nodes
        self.degree = 0
        # Parent, child and sibling to be set later manually
        self.parent = None
        # Points to the leftmost child node
        self.child = None
        # Points to the sibling node immediately to the right
        self.sibling = None

    # Defines the string representation of a node
    def __str__(self):
        parent_key = None
        if self.parent is not None:
            parent_key = self.parent.key
        return '(k=' + str(self.key) + ', p=' + str(parent_key) + ', d=' + str(self.degree) + ')'

    # Function to generate a string representation of all the nodes
    # Depth first from each node in the root list
    # Returns string, a list of the node information
    def walk(self) -> str:
        cat = ""
        node = self
        return self.walk_aux(node, cat)

    # Auxiliary function to walk, please use walk instead
    #  node: Node, the current node in the traversal
    #  cat: str, the string to concatenate node information to
    # Returns string containing string representations of all linked nodes
    def walk_aux(self, node: 'Node', cat: str) -> str:
        if node is None:
            return cat
        else:
            cat += str(node)
            cat += self.walk_aux(node.child, "")
            cat += self.walk_aux(node.sibling, "")
            return cat
