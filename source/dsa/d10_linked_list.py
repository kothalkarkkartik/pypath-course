"""
DSA 10 - Linked lists
=====================

Today's goal:
  1. See what a linked list is: small boxes joined by arrows
  2. Build one yourself with a Node class
  3. Walk through it, insert at the front and reverse it
  4. Find a cycle and merge two sorted lists

A list vs a linked list:
  Python list: the values sit side by side in memory, so Python can jump
  to any item instantly. Linked list: every value lives in its own small
  box (a Node) that holds the value and the address of the next box.

```python
def __init__(self, value, next=None):
    self.value = value    # the data inside the box
    self.next = next      # where the next box lives (or None)
```

So a list is a chain:  A -> B -> C -> None
  You only keep the FIRST box (the head) and the last box points to None.

Walking the list - the three lines you must know:
```python
node = head
while node is not None:
    print(node.value)
    node = node.next          # jump to the next box
```
  Always check `is not None`, never `while node:` - a Node is truthy.

Why linked lists? Putting a new box at the front is instant: O(1).

Reversing a list: use three pointers - prev (None), current (head) and
next_node. Save the next box, point the current box backwards, move on.

Finding a cycle (fast and slow pointers): walk two pointers, the slow
one moves one box and the fast one moves two. If they meet, cycle.

Time complexity in plain words:
  insert at the front  -> O(1), instant
  walk the whole list  -> O(n), one box at a time
  reverse              -> O(n), one pass

Tip: draw the boxes and the arrows on paper first, then change one arrow
at a time and write down what every arrow points to.
"""

from _dsa_kit import main


class Node:
    """One box of a linked list: it holds a value and a link to the next box."""

    def __init__(self, value, next=None):
        self.value = value
        self.next = next

    def __repr__(self) -> str:
        return f"Node({self.value!r})"

    def __eq__(self, other) -> bool:
        # Two lists are equal when they hold the same values in the same order.
        if isinstance(other, Node):
            return list_to_array(self) == list_to_array(other)
        if isinstance(other, list):
            return list_to_array(self) == other
        return NotImplemented


def build_list(values: list) -> Node | None:
    """Build a linked list from a list of values and return the head box.

    build_list([1, 2, 3]) -> Node(1) -> Node(2) -> Node(3) -> None
    """
    head = None
    tail = None
    for value in values:
        box = Node(value)
        if tail is None:
            head = box
        else:
            tail.next = box
        tail = box
    return head


def list_to_array(head: Node | None) -> list:
    """Helper (not an exercise): turn a linked list into a plain list.

    list_to_array(build_list([1, 2, 3])) -> [1, 2, 3]
    """
    values = []
    node = head
    while node is not None:
        values.append(node.value)
        node = node.next
    return values


def build_cycle(values: list) -> Node | None:
    """Helper (not an exercise): build a list whose last box points back."""
    head = build_list(values)
    if head is None:
        return None
    tail = head
    while tail.next is not None:
        tail = tail.next
    tail.next = head          # close the loop
    return head


# ---------------------------------------------------------------------------
# DEMOS - run these first, then change the code and experiment
# ---------------------------------------------------------------------------


def demo_build_list() -> None:
    # Build a chain of boxes: A -> B -> C -> None
    head = build_list(["A", "B", "C"])
    node = head
    while node is not None:
        print(f"box holds {node.value!r} -> next box is {node.next}")
        node = node.next


def demo_traverse() -> None:
    # Walk the list from the head box to the end.
    head = build_list([10, 20, 30, 40])
    total = 0
    node = head
    while node is not None:
        print("value:", node.value)
        total += node.value
        node = node.next
    print("sum of all the values:", total)


def demo_insert_head() -> None:
    # A new box at the front becomes the new head. That is instant.
    head = build_list([2, 3, 4])
    print("before:", list_to_array(head))
    head = Node(1, head)
    print("after inserting 1 at the front:", list_to_array(head),
          "- we changed one arrow, so this is O(1)")


def demo_reverse() -> None:
    # Reverse the list by flipping every arrow one by one.
    head = build_list([1, 2, 3, 4])
    print("before:", list_to_array(head))
    prev = None
    current = head
    while current is not None:
        next_node = current.next     # remember where we were going
        current.next = prev          # flip the arrow backwards
        prev = current               # step the pointers forward
        current = next_node
    print("after :", list_to_array(prev), "- one pass, so O(n)")


def demo_detect_cycle() -> None:
    # Two pointers walk at different speeds.
    def detect(head):
        slow = fast = head
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False

    print("a straight list has a cycle?", detect(build_list([1, 2, 3, 4])))
    print("after closing the loop:", detect(build_cycle([1, 2, 3, 4])))


def demo_merge_two_lists() -> None:
    # Merge two sorted lists by always taking the smaller head.
    a = build_list([1, 3, 5, 7])
    b = build_list([2, 4, 6])
    merged = []
    while a is not None and b is not None:
        if a.value <= b.value:
            merged.append(a.value)
            a = a.next
        else:
            merged.append(b.value)
            b = b.next
    rest = a if a is not None else b
    merged.extend(list_to_array(rest))   # what is left is already sorted
    print("merged values:", merged)


# ---------------------------------------------------------------------------
# EXERCISES - write your code where you see TODO
# ---------------------------------------------------------------------------


def list_length(head: Node | None) -> int:
    """Return how many boxes the list has.

    list_length(build_list([1, 2, 3])) -> 3
    """
    # TODO: walk the list and count the boxes
    return None


def reverse_list(head: Node | None) -> Node | None:
    """Return the head of the list with all the boxes in the opposite order.

    reverse_list(build_list([1, 2, 3])) -> [3, 2, 1]
    """
    # TODO: flip every arrow with the prev / current / next pattern
    return None


def has_cycle(head: Node | None) -> bool:
    """Return True when the list loops back on itself.

    has_cycle(build_list([1, 2, 3])) -> False
    """
    # TODO: walk one pointer one box and another pointer two boxes
    return None


def middle_node_value(head: Node | None):
    """Return the value of the middle box, or None for an empty list.

    middle_node_value(build_list([1, 2, 3])) -> 2
    """
    # TODO: use the fast and the slow pointer together
    return None


def merge_two_lists(a: Node | None, b: Node | None) -> Node | None:
    """Join two sorted lists into one sorted list and return its head.

    merge_two_lists(build_list([1, 3]), build_list([2, 4])) -> [1, 2, 3, 4]
    """
    # TODO: take the smaller head again and again until one list is empty
    return None


def insert_at_head(head: Node | None, value) -> Node | None:
    """Return a new head with value as the first box.

    insert_at_head(build_list([2, 3]), 1) -> [1, 2, 3]
    """
    # TODO: make a new box that points to the old head
    return None


# Solutions - try it yourself first, then run with `--solutions`
def sol_list_length(head: Node | None) -> int:
    count = 0
    node = head
    while node is not None:
        count += 1
        node = node.next
    return count


def sol_reverse_list(head: Node | None) -> Node | None:
    prev = None
    current = head
    while current is not None:
        next_node = current.next     # remember where we were going
        current.next = prev          # flip the arrow backwards
        prev = current
        current = next_node
    return prev


def sol_has_cycle(head: Node | None) -> bool:
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


def sol_middle_node_value(head: Node | None):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow.value if slow is not None else None


def sol_merge_two_lists(a: Node | None, b: Node | None) -> Node | None:
    head = None
    tail = None
    while a is not None or b is not None:
        if b is None or (a is not None and a.value <= b.value):
            value, a = a.value, a.next     # take from the first list
        else:
            value, b = b.value, b.next     # take from the second list
        box = Node(value)
        if tail is None:
            head = box
        else:
            tail.next = box
        tail = box
    return head


def sol_insert_at_head(head: Node | None, value) -> Node | None:
    return Node(value, head)


EXERCISES = [
    {
        "id": "10.1", "task": "list_length(head): how many boxes the list has",
        "func": list_length, "tests": [((build_list([1, 2, 3]),), 3), ((build_list([5]),), 1), ((None,), 0)],
        "solution": sol_list_length,
    },
    {
        "id": "10.2", "task": "reverse_list(head): the values in the opposite order",
        "func": reverse_list, "tests": [((build_list([1, 2, 3]),), [3, 2, 1]), ((build_list([1]),), [1])],
        "solution": sol_reverse_list,
    },
    {
        "id": "10.3", "task": "has_cycle(head): True when the list loops back",
        "func": has_cycle, "tests": [((build_list([1, 2, 3]),), False), ((build_cycle([1, 2, 3]),), True)],
        "solution": sol_has_cycle,
    },
    {
        "id": "10.4", "task": "middle_node_value(head): the value of the middle box",
        "func": middle_node_value, "tests": [((build_list([1, 2, 3]),), 2), ((build_list([1, 2, 3, 4, 5]),), 3)],
        "solution": sol_middle_node_value,
    },
    {
        "id": "10.5", "task": "merge_two_lists(a, b): one sorted list out of two",
        "func": merge_two_lists, "tests": [((build_list([1, 3, 5]), build_list([2, 4, 6])), [1, 2, 3, 4, 5, 6]), ((build_list([]), build_list([1, 2])), [1, 2])],
        "solution": sol_merge_two_lists,
    },
    {
        "id": "10.6", "task": "insert_at_head(head, value): a new first box",
        "func": insert_at_head, "tests": [((build_list([2, 3]), 1), [1, 2, 3]), ((None, 7), [7])],
        "solution": sol_insert_at_head,
    },
]

DEMOS = [
    ("1. Build a linked list", demo_build_list),
    ("2. Walk through it", demo_traverse),
    ("3. Insert at the front", demo_insert_head),
    ("4. Reverse the list", demo_reverse),
    ("5. Find a cycle", demo_detect_cycle),
    ("6. Merge two sorted lists", demo_merge_two_lists),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
