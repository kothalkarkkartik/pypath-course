"""
DSA 12 - Binary trees and BST
==============================

Today's goal:
  1. Understand nodes, roots, children and leaves
  2. Build a tree from a flat list
  3. Walk a tree in 4 different orders
  4. Measure the height of a tree
  5. Flip a tree (mirror it)
  6. Use a binary search tree (BST) to search very fast

A tree is a bunch of nodes joined by edges:
  - A node holds a value and points to at most 2 children.
  - The node at the very top is the ROOT, a node with no children is a LEAF.

The shape of the code:
```python
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left      # left child, or None
        self.right = right    # right child, or None
```

4 ways to walk a tree:
  inorder    : left, node, right  -> sorted values if it is a BST
  preorder   : node, left, right  -> copy the tree
  postorder  : left, right, node  -> delete the tree
  level order: row by row, top to bottom (use a queue)

The 3 recursive walks are the same recipe:
  1. If the node is None, stop (that is the base case).
  2. Walk the left child.
  3. Do the work on the node.
  4. Walk the right child.
  Only the order of steps 2, 3 and 4 changes. That is the whole trick.

Height = the number of nodes on the longest path from root to leaf.
  height(node) = 1 + max(height(left), height(right))
  An empty tree has height 0.

BST rules (only 2 rules, remember them):
  1. Everything in the LEFT subtree is smaller than the node.
  2. Everything in the RIGHT subtree is bigger than the node.
  Because of this, a search throws away half of the tree at every step.
  That is O(log n) - the log comes from the tree getting half as big.

Tip: draw the tree on paper first, then write the code.
Tip: a tree problem is a recursion problem in disguise - the base case
  is always "if node is None, stop".
"""

from collections import deque

from _dsa_kit import main


# The building blocks - a node, a tree and a few helpers


class TreeNode:
    """One node of a binary tree: a value and up to two children."""

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"TreeNode({self.value!r})"

    def __eq__(self, other) -> bool:
        """Compare two trees by their inorder values (a list works too)."""
        if isinstance(other, TreeNode):
            return sol_inorder(self) == sol_inorder(other)
        if isinstance(other, list):
            return sol_inorder(self) == other
        return NotImplemented

    __hash__ = object.__hash__      # the nodes stay hashable


def build_tree(values: list) -> TreeNode:
    """Build a binary tree from a level order list. None means no child."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def print_tree(root, level: int = 0) -> None:
    """Print a tree sideways so you can see its shape."""
    if root is None:
        return
    print("    " * level + str(root.value))
    print_tree(root.left, level + 1)
    print_tree(root.right, level + 1)


def insert_bst(root, value) -> TreeNode:
    """Insert a value into a binary search tree and return the root."""
    if root is None:
        return TreeNode(value)
    if value < root.value:
        root.left = insert_bst(root.left, value)
    else:
        root.right = insert_bst(root.right, value)
    return root


def search_bst(root, value) -> bool:
    """Return True if the value is inside the binary search tree."""
    while root is not None:
        if value == root.value:
            return True
        root = root.left if value < root.value else root.right
    return False


# ---------------------------------------------------------------------------
# DEMOS - run these first, then change the code and experiment
# ---------------------------------------------------------------------------


def demo_build_tree() -> None:
    # The list is read level by level: root, children, grandchildren.
    # None means that child is not there.
    values = [5, 3, 8, 1, 4, 7, 9]
    root = build_tree(values)
    print("level order list:", values, "-> the same tree:")
    print_tree(root)
    print("the tree has", sol_count_nodes(root), "nodes")


def demo_traversals() -> None:
    # 3 ways to walk a tree - only the order of the steps changes.
    root = build_tree([5, 3, 8, 1, 4, 7, 9])
    print("inorder (left, node, right):", sol_inorder(root), "- sorted on a BST")
    print("preorder (node, left, right):", sol_preorder(root))
    print("level order (row by row):", sol_level_order(root))


def demo_tree_height() -> None:
    # The height is the longest path down to a leaf.
    root = build_tree([5, 3, 8, 1, 4, 7, 9, None, None, 2])
    print_tree(root)
    print("height =", sol_tree_height(root), "(nodes on the longest path)")


def demo_invert_tree() -> None:
    # Swap left and right everywhere - the tree becomes a mirror image.
    root = build_tree([4, 2, 7, 1, 3, 6, 9])
    print("before:")
    print_tree(root)
    print("after inverting:")
    print_tree(sol_invert_tree(root))


def demo_bst_insert_and_search() -> None:
    # Insert always goes left for smaller values, right for bigger ones.
    root = None
    for value in [50, 30, 70, 20, 40, 60, 80]:
        root = insert_bst(root, value)
    print("the BST:")
    print_tree(root)
    print("inorder (sorted):", sol_inorder(root))
    print("search 40 ->", search_bst(root, 40), " search 55 ->", search_bst(root, 55))


def demo_count_nodes() -> None:
    # Count the nodes: 1 for this node, plus the two subtrees.
    root = build_tree([5, 3, 8, 1, 4, 7, 9])
    print("the tree has", sol_count_nodes(root), "nodes")


# ---------------------------------------------------------------------------
# EXERCISES - write your code where you see TODO
# ---------------------------------------------------------------------------


def inorder(root) -> list:
    """Return the values in inorder (left, node, right).
    Example: inorder(build_tree([1, 2, 3])) -> [2, 1, 3]"""
    # TODO: walk the left child, add the value, walk the right child
    return None


def preorder(root) -> list:
    """Return the values in preorder (node, left, right).
    Example: preorder(build_tree([1, 2, 3])) -> [1, 2, 3]"""
    # TODO: add the value first, then walk the left and right child
    return None


def level_order(root) -> list:
    """Return the values row by row, from the top down.
    Example: level_order(build_tree([1, 2, 3])) -> [1, 2, 3]"""
    # TODO: use a queue, take the first node, add its children
    return None


def tree_height(root) -> int:
    """Return the height of the tree (nodes on the longest path).
    Example: tree_height(build_tree([1, 2, 3])) -> 2"""
    # TODO: 1 + the bigger height of the two subtrees
    return None


def invert_tree(root):
    """Return the tree mirrored - every left and right child swapped.
    Example: invert_tree(build_tree([1, 2, 3])) -> the tree 3 -> (2, 1)"""
    # TODO: swap the left and right child of every node
    return None


def is_bst(root) -> bool:
    """Return True if the tree is a valid binary search tree.
    Example: is_bst(build_tree([2, 1, 3])) -> True"""
    # TODO: every left value must be smaller, every right value bigger
    return None


def count_nodes(root) -> int:
    """Return how many nodes the tree has.
    Example: count_nodes(build_tree([1, 2, 3])) -> 3"""
    # TODO: 1 plus the nodes of the left and the right subtree
    return None


def is_same_tree(a, b) -> bool:
    """Return True if both trees have the same shape and the same values.
    Example: is_same_tree(build_tree([1, 2]), build_tree([1, 2])) -> True"""
    # TODO: compare the values, then compare both subtrees
    return None


# Solutions - try it yourself first, then run with `--solutions`
def sol_inorder(root) -> list:
    if root is None:
        return []
    return sol_inorder(root.left) + [root.value] + sol_inorder(root.right)


def sol_preorder(root) -> list:
    if root is None:
        return []
    return [root.value] + sol_preorder(root.left) + sol_preorder(root.right)


def sol_level_order(root) -> list:
    if root is None:
        return []
    out = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        out.append(node.value)
        queue += [c for c in (node.left, node.right) if c is not None]
    return out


def sol_tree_height(root) -> int:
    if root is None:
        return 0
    return 1 + max(sol_tree_height(root.left), sol_tree_height(root.right))


def sol_invert_tree(root):
    if root is None:
        return None
    root.left, root.right = sol_invert_tree(root.right), sol_invert_tree(root.left)
    return root


def sol_is_bst(root) -> bool:
    # A tree is a BST when its inorder values are strictly increasing.
    values = sol_inorder(root)
    return all(values[i] < values[i + 1] for i in range(len(values) - 1))


def sol_count_nodes(root) -> int:
    if root is None:
        return 0
    return 1 + sol_count_nodes(root.left) + sol_count_nodes(root.right)


def sol_is_same_tree(a, b) -> bool:
    if a is None or b is None:
        return a is b
    return (a.value == b.value and sol_is_same_tree(a.left, b.left)
            and sol_is_same_tree(a.right, b.right))


EXERCISES = [
    {
        "id": "12.1", "task": "inorder(root): values in left, node, right order",
        "func": inorder, "tests": [((build_tree([2, 1, 3]),), [1, 2, 3])],
        "solution": sol_inorder,
    },
    {
        "id": "12.2", "task": "preorder(root): values in node, left, right order",
        "func": preorder, "tests": [((build_tree([2, 1, 3]),), [2, 1, 3])],
        "solution": sol_preorder,
    },
    {
        "id": "12.3", "task": "level_order(root): values row by row, top down",
        "func": level_order, "tests": [((build_tree([3, 9, 20, None, None, 15, 7]),), [3, 9, 20, 15, 7])],
        "solution": sol_level_order,
    },
    {
        "id": "12.4", "task": "tree_height(root): nodes on the longest path",
        "func": tree_height, "tests": [((build_tree([2, 1, 3]),), 2), ((None,), 0)],
        "solution": sol_tree_height,
    },
    {
        "id": "12.5", "task": "invert_tree(root): mirror the tree (left and right swapped)",
        "func": invert_tree, "tests": [((build_tree([4, 2, 7, 1, 3, 6, 9]),), [9, 7, 6, 4, 3, 2, 1])],
        "solution": sol_invert_tree,
    },
    {
        "id": "12.6", "task": "is_bst(root): check the two BST rules",
        "func": is_bst, "tests": [((build_tree([5, 3, 8, 1, 4, 7, 9]),), True), ((build_tree([5, 1, 4, None, None, 3, 6]),), False)],
        "solution": sol_is_bst,
    },
    {
        "id": "12.7", "task": "count_nodes(root): how many nodes the tree has",
        "func": count_nodes, "tests": [((build_tree([2, 1, 3]),), 3), ((None,), 0)],
        "solution": sol_count_nodes,
    },
    {
        "id": "12.8", "task": "is_same_tree(a, b): are the two trees identical",
        "func": is_same_tree, "tests": [((build_tree([1, 2, 3]), build_tree([1, 2, 3])), True), ((build_tree([1, 2]), build_tree([1, None, 2])), False)],
        "solution": sol_is_same_tree,
    },
]

DEMOS = [
    ("1. Build a tree from a list", demo_build_tree),
    ("2. The 3 walks of a tree", demo_traversals),
    ("3. Height of a tree", demo_tree_height),
    ("4. Invert (mirror) a tree", demo_invert_tree),
    ("5. BST insert and search", demo_bst_insert_and_search),
    ("6. Count the nodes", demo_count_nodes),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
