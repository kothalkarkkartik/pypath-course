"""
Chapter 08 - Tuples and Sets
============================

Today's goal:
  1. Tuple: a list you cannot change (immutable)
  2. Tuple unpacking and multiple return values
  3. Set: a collection of unique items
  4. Set operations: union, intersection, difference
  5. When to use which one

Tuple:
  point = (10, 20)
  single = (5,)          # the comma is required!
  x, y = point           # unpacking
  a, b = b, a            # swap

Set:
  s = {1, 2, 2, 3}       # duplicates remove themselves -> {1, 2, 3}
  s.add(4), s.discard(2)
  a | b   union
  a & b   intersection (in both)
  a - b   difference (in a but not in b)
  a ^ b   symmetric difference (only in one)

A set is fast for membership checks: `x in set` is like O(1), while in a list it is O(n).
Set items must be hashable (you cannot put a list in a set).
"""

from _kit import main
from collections import namedtuple


# ---------------------------------------------------------------------------
# DEMOS
# ---------------------------------------------------------------------------


def demo_tuple() -> None:
    point = (10, 20)
    print("point:", point, "| type:", type(point).__name__)
    print("point[0]:", point[0], "| point[-1]:", point[-1])
    print("len:", len(point))

    # A one-element tuple - the comma is required
    not_tuple = (5)
    real_tuple = (5,)
    print("(5) type:", type(not_tuple).__name__)
    print("(5,) type:", type(real_tuple).__name__)

    # Unpacking
    x, y = point
    print("x:", x, "y:", y)

    # Multiple return values (it is really a tuple)
    def min_max(nums):
        return min(nums), max(nums)

    result = min_max([4, 1, 9, 3])
    print("min_max result:", result)
    low, high = result
    print("low:", low, "high:", high)

    # Immutability
    try:
        point[0] = 99
    except TypeError as e:
        print("TypeError:", e)

    # Tuple methods
    nums = (1, 2, 2, 3)
    print("count(2):", nums.count(2), "| index(3):", nums.index(3))

    # A tuple as a dictionary key (a list cannot be one)
    distances = {("Delhi", "Mumbai"): 1400, ("Delhi", "Jaipur"): 280}
    print("Delhi-Mumbai:", distances[("Delhi", "Mumbai")])

    # namedtuple - fields with names
    Point = namedtuple("Point", ["x", "y"])
    p = Point(3, 4)
    print("namedtuple:", p, "| p.x:", p.x)


def demo_set_basics() -> None:
    nums = [1, 2, 2, 3, 3, 3, 4]
    unique = set(nums)
    print("list:", nums)
    print("set:", unique)
    print("unique count:", len(unique))

    s = {1, 2, 3}
    s.add(4)
    print("add(4):", s)
    s.discard(2)          # no error even if the item is missing
    print("discard(2):", s)
    s.remove(3)           # KeyError if the item is missing
    print("remove(3):", s)

    print("3 in s:", 3 in s)
    print("100 in s:", 100 in s)

    # Make an empty set like this ({} is a dict!)
    empty = set()
    print("empty set:", empty, type(empty).__name__)

    # A set is not ordered, so the print order can be different
    print("set from string:", set("banana"))


def demo_set_ops() -> None:
    a = {1, 2, 3, 4}
    b = {3, 4, 5, 6}

    print("a:", a, "b:", b)
    print("union a | b        :", a | b)
    print("intersection a & b :", a & b)
    print("difference a - b   :", a - b)
    print("difference b - a   :", b - a)
    print("symmetric a ^ b    :", a ^ b)

    print("subset:", {1, 2}.issubset(a))
    print("superset:", a.issuperset({1, 2}))
    print("disjoint:", a.isdisjoint({7, 8}))

    # Also with methods
    print("a.union(b):", a.union(b))
    print("a.intersection(b):", a.intersection(b))


def demo_set_use_cases() -> None:
    # Removing duplicates
    words = ["apple", "banana", "apple", "cherry"]
    print("unique words:", set(words))

    # What two lists have in common
    python_devs = {"Ravi", "Sita", "Amit"}
    dsa_devs = {"Sita", "Neha", "Amit"}
    print("known by both:", python_devs & dsa_devs)
    print("python only:", python_devs - dsa_devs)

    # Fast membership
    allowed = {"admin", "editor", "viewer"}
    print("'admin' allowed:", "admin" in allowed)

    # A frozenset is immutable, so it can be a dict key
    fs = frozenset([1, 2, 3])
    print("frozenset:", fs, "| hashable:", hash(fs) is not None)


# ---------------------------------------------------------------------------
# EXERCISES
# ---------------------------------------------------------------------------


def min_max(nums: list):
    """Return a (min, max) tuple.
    min_max([4, 1, 9]) -> (1, 9)
    """
    # TODO
    return None


def unique_count(nums: list) -> int:
    """How many unique numbers there are."""
    # TODO: len(set(nums))
    return None


def common_elements(a: list, b: list) -> list:
    """The elements common to both lists, as a sorted list.
    common_elements([1, 2, 3], [2, 3, 4]) -> [2, 3]
    """
    # TODO: set intersection + sorted
    return None


def is_subset(a: list, b: list) -> bool:
    """Every element of a must be in b."""
    # TODO
    return None


def unique_sorted(nums: list) -> list:
    """A unique + sorted list."""
    # TODO
    return None


def symmetric_diff(a: list, b: list) -> list:
    """The items that are in only one list (not in both), sorted."""
    # TODO
    return None


# Solutions
def sol_min_max(nums: list):
    return (min(nums), max(nums))


def sol_unique_count(nums: list) -> int:
    return len(set(nums))


def sol_common_elements(a: list, b: list) -> list:
    return sorted(set(a) & set(b))


def sol_is_subset(a: list, b: list) -> bool:
    return set(a).issubset(set(b))


def sol_unique_sorted(nums: list) -> list:
    return sorted(set(nums))


def sol_symmetric_diff(a: list, b: list) -> list:
    return sorted(set(a) ^ set(b))


EXERCISES = [
    {"id": "8.1", "task": "min_max(nums): (min, max) tuple", "func": min_max,
     "tests": [(([4, 1, 9],), (1, 9)), (([5],), (5, 5))], "solution": sol_min_max},
    {"id": "8.2", "task": "unique_count(nums): count of unique items", "func": unique_count,
     "tests": [(([1, 2, 2, 3],), 3), (([],), 0)], "solution": sol_unique_count},
    {"id": "8.3", "task": "common_elements(a, b): common items, sorted", "func": common_elements,
     "tests": [(([1, 2, 3], [2, 3, 4]), [2, 3]), (([1], [2]), [])],
     "solution": sol_common_elements},
    {"id": "8.4", "task": "is_subset(a, b): is all of a inside b?", "func": is_subset,
     "tests": [(([1, 2], [1, 2, 3]), True), (([1, 4], [1, 2, 3]), False)],
     "solution": sol_is_subset},
    {"id": "8.5", "task": "unique_sorted(nums): unique + sorted", "func": unique_sorted,
     "tests": [(([3, 1, 3, 2],), [1, 2, 3])], "solution": sol_unique_sorted},
    {"id": "8.6", "task": "symmetric_diff(a, b): items in only one list", "func": symmetric_diff,
     "tests": [(([1, 2, 3], [2, 3, 4]), [1, 4])], "solution": sol_symmetric_diff},
]

DEMOS = [
    ("8. Tuple", demo_tuple),
    ("9. Set basics", demo_set_basics),
    ("10. Set operations", demo_set_ops),
    ("11. Set use cases", demo_set_use_cases),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
