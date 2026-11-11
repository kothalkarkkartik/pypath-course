"""
DSA 02 - Arrays and basic searching
===================================

Today's goal:
  1. See what an array is and how a Python list works as an array
  2. Walk through a list and add up all the numbers
  3. Find the biggest and the smallest value
  4. Find the second biggest value
  5. Rotate an array to the left
  6. Build prefix sums (running totals)
  7. Count how many times a value shows up

What is an array?
  An array is a row of boxes that all hold the same kind of value.
  In Python we use a `list` for this. The values keep the order you put
  them in, and every box has a number called its index. Indexing starts
  at 0.

    scores = [70, 90, 85]
      index:  0   1   2

  Three things to remember:
  1. The first item is at index 0, not 1.
  2. The last item is at index -1 - that is really handy.
  3. `arr[0]` is the first item and `arr[-1]` is the last one.

The four patterns you will use again and again:
  1. Traverse - go over every item once
  2. Track   - keep a running value (sum, max, min)
  3. Count   - count how many times something happens
  4. Search  - look for one value and stop when you find it

The shape of the code:
```python
total = 0
for value in arr:      # one step per item
    total += value     # keep updating a running total
```

Why this is fast:
  We walk the list exactly one time, so the time is O(n). "n" means the
  number of items. A list with 1000 items means 1000 steps, never more.

Prefix sums - a small super power:
  A prefix sum is the total of everything up to a position.

    arr:        [1, 2, 3, 4]
    prefix:  [1, 3, 6, 10]

  Now the sum of the items 2..4 is just prefix[3] - prefix[1] = 10 - 3 = 7.
  One prefix list turns many range questions into one subtraction.

Tip: write the index numbers under your array before you code.
Tip: always ask "what happens when the array is empty?" before you code.
"""

from collections import Counter

from _dsa_kit import main


# ---------------------------------------------------------------------------
# DEMOS - run these first, then change the code and experiment
# ---------------------------------------------------------------------------


def demo_traverse_and_sum() -> None:
    # The most common loop in DSA: walk the list, keep a running total.
    scores = [70, 90, 85, 60]
    total = 0
    for score in scores:
        total += score
        print(f"  after adding {score:>3}: total = {total}")
    print("  final total =", total)


def demo_max_and_min() -> None:
    # One single loop can find both the biggest and the smallest value.
    prices = [42, 7, 19, 99, 3]
    biggest = prices[0]
    smallest = prices[0]
    for price in prices:
        if price > biggest:
            biggest = price
        if price < smallest:
            smallest = price
    print("  list:     ", prices)
    print("  biggest:  ", biggest)
    print("  smallest: ", smallest)
    # Python has max() and min() built in, but write the loop yourself first.


def demo_second_largest() -> None:
    # The second biggest *different* value, found in one walk.
    numbers = [12, 7, 45, 45, 30]
    biggest = None
    second = None
    for number in numbers:
        if biggest is None or number > biggest:
            second = biggest       # the old biggest becomes the second
            biggest = number
        elif number != biggest and (second is None or number > second):
            second = number
    print("  list:   ", numbers)
    print("  biggest:", biggest)
    print("  second: ", second)
    print("  note: 45 shows up twice, but it is still only one value.")


def demo_rotate_array() -> None:
    # Rotate left by k means: the first k items jump over to the end.
    arr = [1, 2, 3, 4, 5]
    k = 2
    rotated = arr[k:] + arr[:k]
    print("  original:        ", arr)
    print(f"  rotate left {k}:  ", rotated)
    # Two slices and one + is all a rotation needs.


def demo_prefix_sums() -> None:
    # Prefix sums are running totals.
    arr = [2, 3, 5, 7]
    prefix = []
    running = 0
    for value in arr:
        running += value
        prefix.append(running)
    print("  arr:    ", arr)
    print("  prefix:", prefix)
    # Sum of index 1 up to 2 = prefix[2] - prefix[1] = 10 - 5 = 5
    print("  sum of index 1..2 =", prefix[2] - prefix[1])


def demo_frequency_counting() -> None:
    # A dict remembers how many times each value showed up.
    votes = ["a", "b", "a", "c", "b", "a"]
    counts = {}
    for vote in votes:
        counts[vote] = counts.get(vote, 0) + 1
    print("  votes: ", votes)
    print("  counts:", counts)
    print("  most common:", max(counts, key=counts.get))
    # Python has a shortcut for this:
    print("  Counter:", Counter(votes))


# ---------------------------------------------------------------------------
# EXERCISES - write your code where you see TODO
# ---------------------------------------------------------------------------


def sum_array(arr: list) -> int:
    """Return the sum of all the numbers in arr.

    sum_array([1, 2, 3, 4]) -> 10
    """
    # TODO: walk the list and add every number
    return None


def max_array(arr: list):
    """Return the biggest number in arr (None if arr is empty).

    max_array([3, 9, 2]) -> 9
    """
    # TODO: keep track of the biggest value while walking the list
    return None


def second_largest(arr: list):
    """Return the second biggest *different* value, or None if there is none.

    second_largest([10, 20, 15]) -> 15
    """
    # TODO: keep the biggest and the second biggest in one walk
    return None


def rotate_left(arr: list, k: int) -> list:
    """Return a new list where the first k items moved to the end.

    rotate_left([1, 2, 3, 4, 5], 2) -> [3, 4, 5, 1, 2]
    """
    # TODO: cut the list into two pieces and glue them back in the new order
    return None


def prefix_sums(arr: list) -> list:
    """Return a list of running totals. prefix_sums([1, 2, 3]) -> [1, 3, 6].

    prefix_sums([1, 2, 3]) -> [1, 3, 6]
    """
    # TODO: keep a running total and save it after every step
    return None


def count_occurrences(arr: list, x) -> int:
    """Return how many times x shows up in arr.

    count_occurrences([1, 2, 2, 3], 2) -> 2
    """
    # TODO: count the matches while walking the list
    return None


def linear_search(arr: list, x) -> int:
    """Return the index of the first x in arr, or -1 if x is not there.

    linear_search([4, 8, 15], 8) -> 1
    """
    # TODO: walk the list and return the index where you find x
    return None


# Solutions - try it yourself first, then run with `--solutions`
def sol_sum_array(arr: list) -> int:
    total = 0
    for value in arr:
        total += value
    return total


def sol_max_array(arr: list):
    if not arr:
        return None
    biggest = arr[0]
    for value in arr:
        if value > biggest:
            biggest = value
    return biggest


def sol_second_largest(arr: list):
    biggest = None
    second = None
    for value in arr:
        if biggest is None or value > biggest:
            second = biggest  # the old biggest becomes the second biggest
            biggest = value
        elif value != biggest and (second is None or value > second):
            second = value
    return second


def sol_rotate_left(arr: list, k: int) -> list:
    if not arr:
        return []
    k = k % len(arr)  # a full turn changes nothing
    return arr[k:] + arr[:k]


def sol_prefix_sums(arr: list) -> list:
    prefix = []
    running = 0
    for value in arr:
        running += value
        prefix.append(running)
    return prefix


def sol_count_occurrences(arr: list, x) -> int:
    count = 0
    for value in arr:
        if value == x:
            count += 1
    return count


def sol_linear_search(arr: list, x) -> int:
    for index in range(len(arr)):
        if arr[index] == x:
            return index
    return -1


EXERCISES = [
    {
        "id": "2.1",
        "task": "sum_array(arr): add up all the numbers",
        "func": sum_array,
        "tests": [(([1, 2, 3, 4],), 10), (([],), 0), (([5],), 5)],
        "solution": sol_sum_array,
    },
    {
        "id": "2.2",
        "task": "max_array(arr): the biggest value in the list",
        "func": max_array,
        "tests": [(([3, 9, 2],), 9), (([-5, -2, -9],), -2)],
        "solution": sol_max_array,
    },
    {
        "id": "2.3",
        "task": "second_largest(arr): the second biggest different value",
        "func": second_largest,
        "tests": [(([10, 20, 15],), 15), (([5, 5, 5],), None), (([1, 2],), 1)],
        "solution": sol_second_largest,
    },
    {
        "id": "2.4",
        "task": "rotate_left(arr, k): move the first k items to the end",
        "func": rotate_left,
        "tests": [(([1, 2, 3, 4, 5], 2), [3, 4, 5, 1, 2]), (([1, 2, 3], 5), [3, 1, 2])],
        "solution": sol_rotate_left,
    },
    {
        "id": "2.5",
        "task": "prefix_sums(arr): the running totals of the list",
        "func": prefix_sums,
        "tests": [(([1, 2, 3, 4],), [1, 3, 6, 10]), (([],), [])],
        "solution": sol_prefix_sums,
    },
    {
        "id": "2.6",
        "task": "count_occurrences(arr, x): how many times x shows up",
        "func": count_occurrences,
        "tests": [(([1, 2, 2, 3], 2), 2), (([1, 2, 3], 9), 0)],
        "solution": sol_count_occurrences,
    },
    {
        "id": "2.7",
        "task": "linear_search(arr, x): index of x, or -1",
        "func": linear_search,
        "tests": [(([4, 8, 15, 16], 8), 1), (([4, 8], 1), -1)],
        "solution": sol_linear_search,
    },
]

DEMOS = [
    ("1. Traverse and sum", demo_traverse_and_sum),
    ("2. Max and min", demo_max_and_min),
    ("3. Second largest", demo_second_largest),
    ("4. Rotate an array", demo_rotate_array),
    ("5. Prefix sums", demo_prefix_sums),
    ("6. Frequency counting", demo_frequency_counting),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
