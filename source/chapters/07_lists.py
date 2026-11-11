"""
Chapter 07 - Lists (The most important data structure)
=====================================================

Today's goal:
  1. Making a list, index, slice
  2. Add/remove: append, insert, extend, remove, pop
  3. sort, sorted, reverse
  4. The danger of aliasing (copy vs reference)
  5. enumerate, zip, nested list

A list = an ordered collection that you can change. Square brackets [].
  nums = [10, 20, 30]
  mixed = [1, "two", 3.0, True]    # different types work too
  matrix = [[1, 2], [3, 4]]        # a list inside a list

Index: nums[0], nums[-1]
Slice: nums[0:2] -> a new list

The biggest gotcha:
  a = [1, 2]
  b = a          # b and a are the SAME list!
  b.append(3)    # a changes too
  c = a.copy()   # a real copy (or a[:] / list(a))
"""

from _kit import main


# ---------------------------------------------------------------------------
# DEMOS
# ---------------------------------------------------------------------------


def demo_basics() -> None:
    nums = [10, 20, 30, 40, 50]
    print("nums:", nums, "| len:", len(nums))
    print("nums[0]:", nums[0], "| nums[-1]:", nums[-1])
    print("nums[1:4]:", nums[1:4])
    print("nums[:2]:", nums[:2])
    print("nums[::2]:", nums[::2])
    print("nums[::-1]:", nums[::-1])
    print("20 in nums:", 20 in nums)
    print("sum:", sum(nums), "min:", min(nums), "max:", max(nums))

    # Unpacking
    first, second, *rest = nums
    print("first:", first, "second:", second, "rest:", rest)


def demo_add_remove() -> None:
    fruits = ["apple", "banana"]
    print("start:", fruits)

    fruits.append("mango")          # one item at the end
    print("append:", fruits)

    fruits.insert(1, "orange")      # at an index
    print("insert:", fruits)

    fruits.extend(["kiwi", "pear"])  # join another list
    print("extend:", fruits)

    fruits.remove("banana")         # remove by value (ValueError if not found)
    print("remove:", fruits)

    last = fruits.pop()             # take out the last one
    print("pop():", last, "| remaining:", fruits)

    second_item = fruits.pop(1)     # take out by index
    print("pop(1):", second_item, "| remaining:", fruits)

    del fruits[0]
    print("del [0]:", fruits)

    fruits.clear()
    print("clear:", fruits)


def demo_sort() -> None:
    nums = [4, 1, 3, 2]
    print("original:", nums)

    nums.sort()                  # changes the original list
    print("sort():", nums)

    nums.sort(reverse=True)
    print("reverse sort:", nums)

    words = ["banana", "apple", "cherry"]
    print("sorted(words):", sorted(words))      # a new list, original stays the same
    print("original still:", words)

    # Sorting with a key
    print("by length:", sorted(words, key=len))
    people = [("Ravi", 25), ("Sita", 21), ("Amit", 30)]
    print("by age:", sorted(people, key=lambda p: p[1]))

    # reverse() only flips the order, it does not sort
    nums2 = [1, 2, 3]
    nums2.reverse()
    print("reverse():", nums2)


def demo_alias_copy() -> None:
    a = [1, 2, 3]
    b = a                # alias! the same object
    b.append(4)
    print("a:", a, "b:", b)
    print("a is b:", a is b)

    c = a.copy()         # a new object
    c.append(5)
    print("a:", a, "c:", c)
    print("a is c:", a is c)

    # The shallow copy problem with nested lists
    matrix = [[1, 2], [3, 4]]
    shallow = matrix.copy()
    shallow[0].append(99)
    print("matrix:", matrix)   # the inner list is the same one!
    print("shallow:", shallow)

    # Deep copy
    import copy
    deep = copy.deepcopy(matrix)
    deep[1].append(77)
    print("deep:", deep, "| matrix:", matrix)


def demo_enumerate_zip() -> None:
    names = ["Ravi", "Sita", "Amit"]
    marks = [80, 95, 70]

    for i, name in enumerate(names, start=1):
        print(i, name)

    print("zip:")
    for name, mark in zip(names, marks):
        print(f"  {name}: {mark}")

    print("pairs list:", list(zip(names, marks)))

    # A dictionary from zip
    print(dict(zip(names, marks)))


def demo_nested() -> None:
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
    ]
    print("matrix:", matrix)
    print("matrix[0][1]:", matrix[0][1])

    # Row-wise print
    for row in matrix:
        for value in row:
            print(value, end=" ")
        print()

    # Transpose (turn rows into columns)
    transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
    print("transposed:", transposed)


# ---------------------------------------------------------------------------
# EXERCISES
# ---------------------------------------------------------------------------


def second_largest(nums: list) -> int:
    """The second largest DISTINCT number.
    second_largest([3, 1, 4, 4, 2]) -> 3
    """
    # TODO: sorted(set(nums))[-2]
    return None


def dedupe(nums: list) -> list:
    """Remove duplicates and keep the original order.
    dedupe([1, 2, 1, 3, 2]) -> [1, 2, 3]
    """
    # TODO: loop + "not in", or dict.fromkeys
    return None


def rotate(nums: list, k: int) -> list:
    """Rotate the list k steps to the right (returns a new list).
    rotate([1, 2, 3, 4], 1) -> [4, 1, 2, 3]
    rotate([1, 2, 3, 4], 2) -> [3, 4, 1, 2]
    """
    # TODO: k %= len(nums), then slice
    return None


def flatten(matrix: list) -> list:
    """Turn a list of lists into one flat list.
    flatten([[1, 2], [3, 4]]) -> [1, 2, 3, 4]
    """
    # TODO: a loop or a nested comprehension
    return None


def average(nums: list) -> float:
    """Average; an empty list -> 0.0"""
    # TODO
    return None


def merge_sorted(a: list, b: list) -> list:
    """Merge two sorted lists into one sorted list (sorted() is allowed).
    merge_sorted([1, 3], [2, 4]) -> [1, 2, 3, 4]
    """
    # TODO
    return None


# Solutions
def sol_second_largest(nums: list) -> int:
    return sorted(set(nums))[-2]


def sol_dedupe(nums: list) -> list:
    result = []
    for n in nums:
        if n not in result:
            result.append(n)
    return result


def sol_rotate(nums: list, k: int) -> list:
    if not nums:
        return []
    k %= len(nums)
    return nums[-k:] + nums[:-k]


def sol_flatten(matrix: list) -> list:
    result = []
    for row in matrix:
        result.extend(row)
    return result


def sol_average(nums: list) -> float:
    return sum(nums) / len(nums) if nums else 0.0


def sol_merge_sorted(a: list, b: list) -> list:
    return sorted(a + b)


EXERCISES = [
    {"id": "7.1", "task": "second_largest(nums): the second largest distinct number", "func": second_largest,
     "tests": [(([3, 1, 4, 4, 2],), 3), (([10, 10, 9],), 9)], "solution": sol_second_largest},
    {"id": "7.2", "task": "dedupe(nums): keep the order, remove duplicates", "func": dedupe,
     "tests": [(([1, 2, 1, 3, 2],), [1, 2, 3]), (([5, 5, 5],), [5])], "solution": sol_dedupe},
    {"id": "7.3", "task": "rotate(nums, k): k steps to the right", "func": rotate,
     "tests": [(([1, 2, 3, 4], 1), [4, 1, 2, 3]), (([1, 2, 3, 4], 2), [3, 4, 1, 2]),
               (([1, 2], 0), [1, 2])], "solution": sol_rotate},
    {"id": "7.4", "task": "flatten(matrix): flatten a nested list", "func": flatten,
     "tests": [(([[1, 2], [3, 4]],), [1, 2, 3, 4]), (([[], [1]],), [1])], "solution": sol_flatten},
    {"id": "7.5", "task": "average(nums): average, empty -> 0.0", "func": average,
     "tests": [(([1, 2, 3],), 2.0), (([],), 0.0)], "solution": sol_average},
    {"id": "7.6", "task": "merge_sorted(a, b): merge both lists", "func": merge_sorted,
     "tests": [(([1, 3], [2, 4]), [1, 2, 3, 4]), (([], [1]), [1])], "solution": sol_merge_sorted},
]

DEMOS = [
    ("7. List basics", demo_basics),
    ("8. Add and remove", demo_add_remove),
    ("9. Sorting", demo_sort),
    ("10. Alias vs copy (important!)", demo_alias_copy),
    ("11. enumerate and zip", demo_enumerate_zip),
    ("12. Nested list", demo_nested),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
