"""
DSA 07 - Hashing, dictionaries and sets
========================================

Today's goal:
  1. Use a dictionary as a fast lookup table
  2. Count how many times each value appears (a frequency map)
  3. Solve "two sum" and its friends in one pass
  4. Use sets for quick "is this here?" questions

What is hashing?
  Hashing means turning a value into a spot inside a table, so you can
  ask "have I seen this before?" in O(1) - one step, big data or not.

The most used pattern of all:
```python
counts = {}
for value in arr:
    counts[value] = counts.get(value, 0) + 1
```
  `counts.get(value, 0)` means "give me the count, or 0 if it is not
  there yet". After the loop the dict is a frequency map: O(n) time and
  O(n) space - one entry per different value.

Two sum with a dict:
  Instead of checking every pair (that is O(n * n)), remember where you
  have been. For each value ask: "have I seen the number that would make
  the sum right?" If yes, you have your answer.
```python
seen = {}
for i, value in enumerate(arr):
    need = target - value
    if need in seen:
        return (seen[need], i)
    seen[value] = i
```

Sets:
  A set is a box of unique things: it answers "is this inside?" in O(1)
  and drops duplicates for free.
```python
a = {1, 2, 3}
b = {3, 4}
a | b     # union: everything from both
a & b     # intersection: the things in both
a - b     # difference: in a but not in b
```

Grouping by a key:
  When two items belong in the same group, use the group name as the
  dict key. For anagrams the group name is the sorted letters.

Why it works:
  - A dict lookup is a hash lookup, not a walk through the whole list.
  - A set never keeps a duplicate, so grouping by a key comes for free.

Speed: a frequency map and two sum are both O(n) time and O(n) space.
Grouping anagrams is O(n * k) time, where k is the length of a word.

Tips:
  - `counts[value] = counts.get(value, 0) + 1` is the counting habit.
  - `key in seen` is a fast "have I seen it?" test.
  - `set(list)` removes duplicates in one line.
"""

from _dsa_kit import main


# ---------------------------------------------------------------------------
# DEMOS - run these first, then change the code and experiment
# ---------------------------------------------------------------------------


def demo_frequency_map() -> None:
    # Count how many times each value shows up.
    arr = [2, 5, 2, 8, 5, 2]
    counts = {}
    for value in arr:
        counts[value] = counts.get(value, 0) + 1
    print("array:  ", arr, "counts:", counts)
    print("how many 2s?", counts.get(2, 0), " how many 9s?", counts.get(9, 0))


def demo_two_sum() -> None:
    # Remember where you were, so you never check a pair twice.
    arr = [2, 7, 11, 15]
    target = 9
    seen = {}
    answer = None
    print("array:  ", arr, "target:", target)
    for i, value in enumerate(arr):
        need = target - value
        if need in seen:
            answer = (seen[need], i)
            break
        seen[value] = i
    print("answer: ", answer, "(the numbers 2 and 7 add up to 9)")


def demo_group_anagrams() -> None:
    # Words that use the same letters belong in the same group.
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    groups = {}
    for word in words:
        key = "".join(sorted(word))    # the group name
        groups.setdefault(key, []).append(word)
    print("words: ", words)
    for key, group in groups.items():
        print("  ", key, "->", group)


def demo_subarray_sum_k() -> None:
    # Count the chunks that add up to k, using prefix sums.
    arr = [1, 1, 1]
    k = 2
    counts = {0: 1}
    prefix = 0
    total = 0
    for value in arr:
        prefix += value
        total += counts.get(prefix - k, 0)
        counts[prefix] = counts.get(prefix, 0) + 1
    print("array:", arr, "k:", k)
    print("chunks with sum", k, ":", total)


def demo_set_operations() -> None:
    # Sets are boxes of unique things, so duplicates disappear.
    a = {1, 2, 3, 4}
    b = {3, 4, 5, 6}
    print("a        :", a)
    print("b        :", b)
    print("union    :", sorted(a | b))
    print("both     :", sorted(a & b))
    print("only in a:", sorted(a - b))
    print("in a? 3 ->", 3 in a, "  in a? 9 ->", 9 in a)


def demo_remove_duplicates() -> None:
    # set() drops the duplicates, dict.fromkeys() keeps the order.
    words = ["a", "b", "a", "c", "b"]
    print("words:", words, "-> as a set:", sorted(set(words)))
    print("unique, in order:", list(dict.fromkeys(words)))


# ---------------------------------------------------------------------------
# EXERCISES - write your code where you see TODO
# ---------------------------------------------------------------------------


def two_sum(arr: list, target: int) -> tuple:
    """Return the indexes (i, j) of two numbers that add up to target, or None.

    two_sum([2, 7, 11, 15], 9) -> (0, 1)
    """
    # TODO: remember each number and its index in a dict
    return None


def group_anagrams(words: list) -> list:
    """Return the words grouped by their letters (grouped words keep their order).

    group_anagrams(["eat", "tea", "ate"]) -> [["eat", "tea", "ate"]]
    """
    # TODO: use the sorted letters of a word as the group key
    return None


def subarray_sum_equals_k(arr: list, k: int) -> int:
    """Return how many chunks of neighbours add up to exactly k.

    subarray_sum_equals_k([1, 1, 1], 2) -> 2
    """
    # TODO: use prefix sums and a dict of the sums seen so far
    return None


def first_unique_char_index(s: str) -> int:
    """Return the index of the first letter that appears only once, or None.

    first_unique_char_index("leetcode") -> 0
    """
    # TODO: count the letters, then find the first one with a count of 1
    return None


def intersect_arrays(a: list, b: list) -> list:
    """Return the values that appear in both lists, sorted from small to big.

    intersect_arrays([1, 2, 3, 4], [3, 4, 5]) -> [3, 4]
    """
    # TODO: turn one list into a set, then keep the matches
    return None


def char_counts(s: str) -> dict:
    """Return a dict with every letter and how many times it shows up.

    char_counts("hello") -> {"h": 1, "e": 1, "l": 2, "o": 1}
    """
    # TODO: count the letters in a dict
    return None


def contains_all_chars(s: str) -> bool:
    """Return True when every digit from 0 to 9 shows up somewhere in s.

    contains_all_chars("0123456789") -> True
    """
    # TODO: check that each of the ten digits is inside the string
    return None


# Solutions - try it yourself first, then run with `--solutions`
def sol_two_sum(arr: list, target: int) -> tuple:
    seen = {}
    for i, value in enumerate(arr):
        need = target - value
        if need in seen:
            return (seen[need], i)
        seen[value] = i
    return None


def sol_group_anagrams(words: list) -> list:
    groups = {}
    for word in words:
        key = "".join(sorted(word))
        groups.setdefault(key, []).append(word)
    return list(groups.values())


def sol_subarray_sum_equals_k(arr: list, k: int) -> int:
    counts = {0: 1}
    prefix = 0
    total = 0
    for value in arr:
        prefix += value
        total += counts.get(prefix - k, 0)
        counts[prefix] = counts.get(prefix, 0) + 1
    return total


def sol_first_unique_char_index(s: str) -> int:
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return None


def sol_intersect_arrays(a: list, b: list) -> list:
    other = set(b)
    return sorted({value for value in a if value in other})


def sol_char_counts(s: str) -> dict:
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    return counts


def sol_contains_all_chars(s: str) -> bool:
    for digit in "0123456789":
        if digit not in s:
            return False
    return True


EXERCISES = [
    {
        "id": "7.1",
        "task": "two_sum(arr, target): indexes of two numbers that add up to target",
        "func": two_sum,
        "tests": [(([2, 7, 11, 15], 9), (0, 1)), (([3, 2, 4], 6), (1, 2)), (([1, 2], 10), None)],
        "solution": sol_two_sum,
    },
    {
        "id": "7.2",
        "task": "group_anagrams(words): words grouped by their letters",
        "func": group_anagrams,
        "tests": [
            ((["eat", "tea", "tan", "ate", "nat", "bat"],), [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]),
            ((["a"],), [["a"]]),
            (([""],), [[""]]),
        ],
        "solution": sol_group_anagrams,
    },
    {
        "id": "7.3",
        "task": "subarray_sum_equals_k(arr, k): how many chunks add up to k",
        "func": subarray_sum_equals_k,
        "tests": [(([1, 1, 1], 2), 2), (([1, 2, 3], 3), 2), (([], 0), 0)],
        "solution": sol_subarray_sum_equals_k,
    },
    {
        "id": "7.4",
        "task": "first_unique_char_index(s): index of the first letter seen once",
        "func": first_unique_char_index,
        "tests": [(("leetcode",), 0), (("loveleetcode",), 2), (("aabb",), None)],
        "solution": sol_first_unique_char_index,
    },
    {
        "id": "7.5",
        "task": "intersect_arrays(a, b): the values that appear in both lists",
        "func": intersect_arrays,
        "tests": [(([1, 2, 3, 4], [3, 4, 5]), [3, 4]), ((["a", "b"], ["b", "c"]), ["b"]), (([1, 1, 2], [2, 2]), [2])],
        "solution": sol_intersect_arrays,
    },
    {
        "id": "7.6",
        "task": "char_counts(s): a dict with every letter and its count",
        "func": char_counts,
        "tests": [(("hello",), {"h": 1, "e": 1, "l": 2, "o": 1}), (("",), {})],
        "solution": sol_char_counts,
    },
    {
        "id": "7.7",
        "task": "contains_all_chars(s): True when all ten digits are inside s",
        "func": contains_all_chars,
        "tests": [(("0123456789",), True), (("012345678",), False), (("abc",), False)],
        "solution": sol_contains_all_chars,
    },
]

DEMOS = [
    ("1. Build a frequency map", demo_frequency_map),
    ("2. Two sum with a dict", demo_two_sum),
    ("3. Group anagrams", demo_group_anagrams),
    ("4. Count subarrays with sum k", demo_subarray_sum_k),
    ("5. Set operations", demo_set_operations),
    ("6. Remove duplicates", demo_remove_duplicates),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
