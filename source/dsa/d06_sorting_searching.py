"""
DSA 06 - Sorting and binary search
===================================

Today's goal:
  1. Write bubble sort, selection sort and insertion sort by hand
  2. Learn why the built-in sorted() is much faster than your own code
  3. Use binary search to find a value in O(log n) steps
  4. Find the first spot where a value could sit (lower bound)

Sorting means putting the values in order - smallest first, biggest
last. It is the most common "prep step" in computer science, because
sorted data is easy to search, compare and merge. We write the slow
sorts by hand to see how sorting really works.

How slow are they?
  - Bubble sort: O(n * n) - it makes many passes over the list.
  - Selection sort: O(n * n) - it looks at every pair of spots.
  - Insertion sort: O(n * n) worst case but O(n) on a sorted list.

Python has a fast sort built in:
```python
numbers.sort()          # changes the list in place
copy = sorted(numbers)  # makes a new sorted list
```
  `sort()` and `sorted()` are O(n log n) and they run in fast C code.

Binary search:
  If the list is sorted you do not have to look at every item. Look at
  the middle: too small go right, too big go left. Every step cuts the
  search space in half.
```python
low, high = 0, len(arr) - 1
while low <= high:
    mid = (low + high) // 2
    if arr[mid] < target:
        low = mid + 1
    else:
        high = mid - 1
```
  Binary search is O(log n) - for 1000 items, about 10 steps. A normal
  loop is O(n) - for 1000 items, up to 1000 steps.

Lower bound:
  `lower_bound(arr, x)` gives the first index where x could be placed
  without breaking the order. Use it to count the items smaller than x.

Tips:
  - Binary search only works on a sorted list. Sort first, then search.
  - Use `//` for the middle index, never `/`.
"""

from _dsa_kit import main


# ---------------------------------------------------------------------------
# DEMOS - run these first, then change the code and experiment
# ---------------------------------------------------------------------------


def demo_bubble_sort() -> None:
    # The big values "bubble" up to the end of the list.
    arr = [5, 1, 4, 2, 8]
    for end in range(len(arr) - 1, 0, -1):
        for i in range(end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]   # swap
        print("pass", len(arr) - end, ":", arr)


def demo_selection_sort() -> None:
    # Every pass we look for the smallest item and put it in place.
    arr = [5, 1, 4, 2, 8]
    for i in range(len(arr)):
        smallest = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[smallest]:
                smallest = j
        arr[i], arr[smallest] = arr[smallest], arr[i]   # swap
        print("after step", i + 1, ":", arr)


def demo_insertion_sort() -> None:
    # Like sorting a hand of cards: insert each new card where it fits.
    arr = [5, 1, 4, 2, 8]
    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > current:
            arr[j + 1] = arr[j]      # shift the bigger one right
            j -= 1
        arr[j + 1] = current
        print("after inserting", current, ":", arr)


def demo_builtin_sorted() -> None:
    # Python's own sort: fast, stable and it never breaks your list.
    arr = [5, 1, 4, 2, 8]
    print("original:", arr, "-> sorted(arr):", sorted(arr), "- the list is untouched")
    arr.sort()
    print("after arr.sort():", arr, "- biggest first:", sorted(arr, reverse=True))


def demo_binary_search() -> None:
    # Look in the middle, throw away half of the list, repeat.
    arr = [1, 3, 5, 7, 9, 11, 13]
    target = 11
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        print("  look at index", mid, "value", arr[mid])
        if arr[mid] == target:
            print("  found it at index", mid)
            break
        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    else:
        print("  not found")


def demo_lower_bound() -> None:
    # The first index where the target could sit in the sorted list.
    arr = [1, 3, 5, 7, 9, 11, 13]
    target = 8
    low, high = 0, len(arr)
    while low < high:
        mid = (low + high) // 2
        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid
    print("list:", arr, "- lower bound of", target, "->", low)


# ---------------------------------------------------------------------------
# EXERCISES - write your code where you see TODO
# ---------------------------------------------------------------------------


def bubble_sort(arr: list) -> list:
    """Return a new sorted list (smallest first) and leave the original alone.

    bubble_sort([5, 3, 8, 1]) -> [1, 3, 5, 8]
    """
    # TODO: copy the list, then swap neighbours that are in the wrong order
    return None


def selection_sort(arr: list) -> list:
    """Return a new sorted list (smallest first) and leave the original alone.

    selection_sort([5, 3, 8, 1]) -> [1, 3, 5, 8]
    """
    # TODO: copy the list, then put the smallest item in place again and again
    return None


def insertion_sort(arr: list) -> list:
    """Return a new sorted list (smallest first) and leave the original alone.

    insertion_sort([5, 3, 8, 1]) -> [1, 3, 5, 8]
    """
    # TODO: copy the list, then insert each item into the sorted part
    return None


def binary_search(arr: list, target: int) -> int:
    """Return the index of the target in a sorted list, or -1 if it is not there.

    binary_search([1, 3, 5, 7, 9], 7) -> 3
    """
    # TODO: use low and high and look at the middle
    return None


def lower_bound(arr: list, target: int) -> int:
    """Return the first index where the target fits (len(arr) if it is too big).

    lower_bound([1, 3, 5, 7, 9], 6) -> 3
    """
    # TODO: binary search for the first value that is not smaller
    return None


def count_less_than(arr: list, x: int) -> int:
    """Return how many numbers in arr are strictly smaller than x.

    count_less_than([1, 2, 3, 4], 3) -> 2
    """
    # TODO: look at every number and count the small ones
    return None


def is_sorted(arr: list) -> bool:
    """Return True if the numbers go from small to big (an empty list is sorted).

    is_sorted([1, 2, 3]) -> True
    """
    # TODO: compare every number with the one after it
    return None


# Solutions - try it yourself first, then run with `--solutions`
def sol_bubble_sort(arr: list) -> list:
    numbers = list(arr)
    for end in range(len(numbers) - 1, 0, -1):
        for i in range(end):
            if numbers[i] > numbers[i + 1]:
                numbers[i], numbers[i + 1] = numbers[i + 1], numbers[i]
    return numbers


def sol_selection_sort(arr: list) -> list:
    numbers = list(arr)
    for i in range(len(numbers)):
        smallest = i
        for j in range(i + 1, len(numbers)):
            if numbers[j] < numbers[smallest]:
                smallest = j
        numbers[i], numbers[smallest] = numbers[smallest], numbers[i]
    return numbers


def sol_insertion_sort(arr: list) -> list:
    numbers = list(arr)
    for i in range(1, len(numbers)):
        current = numbers[i]
        j = i - 1
        while j >= 0 and numbers[j] > current:
            numbers[j + 1] = numbers[j]
            j -= 1
        numbers[j + 1] = current
    return numbers


def sol_binary_search(arr: list, target: int) -> int:
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def sol_lower_bound(arr: list, target: int) -> int:
    low, high = 0, len(arr)
    while low < high:
        mid = (low + high) // 2
        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid
    return low


def sol_count_less_than(arr: list, x: int) -> int:
    count = 0
    for value in arr:
        if value < x:
            count += 1
    return count


def sol_is_sorted(arr: list) -> bool:
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True


EXERCISES = [
    {
        "id": "6.1",
        "task": "bubble_sort(arr): new sorted list, the original stays the same",
        "func": bubble_sort,
        "tests": [(([5, 3, 8, 1, 2],), [1, 2, 3, 5, 8]), (([],), []), (([2, 1],), [1, 2])],
        "solution": sol_bubble_sort,
    },
    {
        "id": "6.2",
        "task": "selection_sort(arr): new sorted list, the original stays the same",
        "func": selection_sort,
        "tests": [(([5, 3, 8, 1, 2],), [1, 2, 3, 5, 8]), (([],), []), (([9, 4, 4],), [4, 4, 9])],
        "solution": sol_selection_sort,
    },
    {
        "id": "6.3",
        "task": "insertion_sort(arr): new sorted list, the original stays the same",
        "func": insertion_sort,
        "tests": [(([5, 3, 8, 1, 2],), [1, 2, 3, 5, 8]), (([],), []), (([3, 2, 1],), [1, 2, 3])],
        "solution": sol_insertion_sort,
    },
    {
        "id": "6.4",
        "task": "binary_search(arr, target): index of the target or -1",
        "func": binary_search,
        "tests": [(([1, 3, 5, 7, 9], 7), 3), (([1, 3, 5], 4), -1), (([], 1), -1)],
        "solution": sol_binary_search,
    },
    {
        "id": "6.5",
        "task": "lower_bound(arr, target): first index where the target fits",
        "func": lower_bound,
        "tests": [(([1, 3, 5, 7, 9], 5), 2), (([1, 3, 5, 7, 9], 6), 3), (([1, 3, 5], 9), 3)],
        "solution": sol_lower_bound,
    },
    {
        "id": "6.6",
        "task": "count_less_than(arr, x): how many numbers are smaller than x",
        "func": count_less_than,
        "tests": [(([1, 2, 3, 4], 3), 2), (([5, 1, 3], 3), 1), (([], 5), 0)],
        "solution": sol_count_less_than,
    },
    {
        "id": "6.7",
        "task": "is_sorted(arr): True when the numbers go from small to big",
        "func": is_sorted,
        "tests": [(([1, 2, 3],), True), (([3, 1],), False), (([],), True)],
        "solution": sol_is_sorted,
    },
]

DEMOS = [
    ("1. Bubble sort", demo_bubble_sort),
    ("2. Selection sort", demo_selection_sort),
    ("3. Insertion sort", demo_insertion_sort),
    ("4. The built-in sorted()", demo_builtin_sorted),
    ("5. Binary search", demo_binary_search),
    ("6. Lower bound", demo_lower_bound),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
