"""
DSA 04 - Two pointers
=====================

Today's goal:
  1. Learn the two pointer pattern
  2. Find a pair that adds up to a target in a sorted array
  3. Check a palindrome without cutting the string in half
  4. Remove duplicates from a sorted array
  5. Solve the "container with most water" problem
  6. Reverse a list or a string by swapping the ends

The two pointer idea:
  Some problems need you to look at two different places in the same list.
  One pointer from the left and one from the right does it without nested loops.

    left  ->              <- right
      [1, 3, 5, 7, 9]

  The shape of the loop:
```python
left, right = 0, len(arr) - 1
while left < right:
    total = arr[left] + arr[right]
    if total == target:
        return left, right
    elif total < target:
        left += 1      # need a bigger number, move left one step
    else:
        right -= 1     # need a smaller number, move right one step
```

Why moving one pointer is enough:
  - The total is too small. Then arr[left] + arr[right] is too small, and
    arr[right] is the biggest value still available. So arr[left] can
    never be part of the answer. Throw it away: move left.
  - The total is too big. Then arr[left] + arr[right] is too big, and
    arr[left] is the smallest value still available. So arr[right] can
    never be part of the answer. Throw it away: move right.

  Every step throws away one value that cannot help. The time is O(n) -
  we walk the list once with two pointers at the same time.

Remember: two pointers need sorted data, or a "compare the two ends" check.

Tip: write the array on paper and draw the two arrows.
Tip: always stop when `left >= right`, otherwise you can loop forever.
"""

from _dsa_kit import main


# ---------------------------------------------------------------------------
# DEMOS - run these first, then change the code and experiment
# ---------------------------------------------------------------------------


def demo_pair_sum_sorted() -> None:
    # Two numbers from a sorted array that add up to the target.
    arr = [1, 3, 5, 7, 9]
    target = 10
    left, right = 0, len(arr) - 1
    print("  arr:   ", arr, " target:", target)
    while left < right:
        total = arr[left] + arr[right]
        print(f"    left={left} right={right} -> {arr[left]} + {arr[right]} = {total}")
        if total == target:
            print("    found it at indexes", (left, right))
            break
        elif total < target:
            left += 1
        else:
            right -= 1


def demo_palindrome_two_pointers() -> None:
    # Compare the two ends of the string and move inwards.
    word = "racecar"
    left, right = 0, len(word) - 1
    ok = True
    while left < right:
        if word[left] != word[right]:
            ok = False
            break
        left += 1
        right -= 1
    print("  word:", word, "-> palindrome:", ok)


def demo_remove_duplicates() -> None:
    # The array is sorted, so the duplicates sit next to each other.
    arr = [1, 1, 2, 2, 2, 3, 4, 4]
    result = []
    for value in arr:
        if not result or value != result[-1]:
            result.append(value)
    print("  arr:    ", arr, "\n  unique: ", result)


def demo_container_most_water() -> None:
    # Two vertical lines, the widest pair that holds the most water.
    height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    left, right = 0, len(height) - 1
    best = 0
    print("  height:", height)
    while left < right:
        area = (right - left) * min(height[left], height[right])
        if area > best:
            best = area
        print(f"    left={left} right={right} -> area = {area}  (best = {best})")
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    print("  most water =", best)


def demo_reverse_in_place() -> None:
    # Swap the two ends, then move both pointers towards the middle.
    arr = ["a", "b", "c", "d"]
    print("  before:", arr)
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    print("  after: ", arr)


def demo_two_pointers_vs_loops() -> None:
    # The same job: nested loops first, then two pointers.
    arr = list(range(1, 11))
    target = 12
    nested_steps = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            nested_steps += 1
            if arr[i] + arr[j] == target:
                break
    left, right = 0, len(arr) - 1
    pointer_steps = 0
    while left < right:
        pointer_steps += 1
        if arr[left] + arr[right] == target:
            break
        elif arr[left] + arr[right] < target:
            left += 1
        else:
            right -= 1
    print("  array:  ", arr, " target:", target)
    print("  nested loops did", nested_steps, "steps, two pointers did", pointer_steps)


# ---------------------------------------------------------------------------
# EXERCISES - write your code where you see TODO
# ---------------------------------------------------------------------------


def two_sum_sorted(arr: list, target: int):
    """Return (i, j) with arr[i] + arr[j] == target, or None if there is no pair.

    The array must be sorted. two_sum_sorted([1, 2, 4, 6], 6) -> (1, 2)
    """
    # TODO: start one pointer at each end and move them towards the middle
    return None


def is_palindrome_tp(s: str) -> bool:
    """Return True if s reads the same backwards, using two pointers.

    is_palindrome_tp("level") -> True
    """
    # TODO: compare the first and the last character, then move inwards
    return None


def remove_duplicates(arr: list) -> list:
    """Return the list without duplicates. The array must be sorted.

    remove_duplicates([1, 1, 2, 3, 3]) -> [1, 2, 3]
    """
    # TODO: walk the list and keep a value only when it is different
    return None


def max_area(height: list) -> int:
    """Return the biggest water area two lines can hold.

    max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) -> 49
    """
    # TODO: one pointer at each end, keep the biggest area you find
    return None


def reverse_in_place(arr: list) -> list:
    """Return the reversed list. The list you give us is left untouched.

    reverse_in_place([1, 2, 3]) -> [3, 2, 1]
    """
    # TODO: swap the two ends and move both pointers towards the middle
    return None


def has_pair_with_sum(arr: list, target: int) -> bool:
    """Return True if any two different items add up to the target.

    has_pair_with_sum([1, 2, 4], 6) -> True
    """
    # TODO: sort a copy of the list and use two pointers on it
    return None


# Solutions - try it yourself first, then run with `--solutions`
def sol_two_sum_sorted(arr: list, target: int):
    left, right = 0, len(arr) - 1
    while left < right:
        total = arr[left] + arr[right]
        if total == target:
            return (left, right)
        elif total < target:
            left += 1
        else:
            right -= 1
    return None


def sol_is_palindrome_tp(s: str) -> bool:
    clean = "".join(ch for ch in s.lower() if ch.isalnum())
    left, right = 0, len(clean) - 1
    while left < right:
        if clean[left] != clean[right]:
            return False
        left += 1
        right -= 1
    return True


def sol_remove_duplicates(arr: list) -> list:
    result = []
    for value in arr:
        if not result or value != result[-1]:
            result.append(value)
    return result


def sol_max_area(height: list) -> int:
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        area = (right - left) * min(height[left], height[right])
        if area > best:
            best = area
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return best


def sol_reverse_in_place(arr: list) -> list:
    result = list(arr)  # a copy, so the caller's list stays safe
    left, right = 0, len(result) - 1
    while left < right:
        result[left], result[right] = result[right], result[left]
        left += 1
        right -= 1
    return result


def sol_has_pair_with_sum(arr: list, target: int) -> bool:
    numbers = sorted(arr)
    left, right = 0, len(numbers) - 1
    while left < right:
        total = numbers[left] + numbers[right]
        if total == target:
            return True
        elif total < target:
            left += 1
        else:
            right -= 1
    return False


EXERCISES = [
    {
        "id": "4.1",
        "task": "two_sum_sorted(arr, target): the indexes of the pair, or None",
        "func": two_sum_sorted,
        "tests": [(([1, 2, 4, 6], 6), (1, 2)), (([1, 2, 3], 100), None)],
        "solution": sol_two_sum_sorted,
    },
    {
        "id": "4.2",
        "task": "is_palindrome_tp(s): palindrome check with two pointers",
        "func": is_palindrome_tp,
        "tests": [(("level",), True), (("hello",), False)],
        "solution": sol_is_palindrome_tp,
    },
    {
        "id": "4.3",
        "task": "remove_duplicates(arr): drop the duplicates from a sorted list",
        "func": remove_duplicates,
        "tests": [(([1, 1, 2, 3, 3],), [1, 2, 3]), (([5],), [5])],
        "solution": sol_remove_duplicates,
    },
    {
        "id": "4.4",
        "task": "max_area(height): the biggest water area two lines can hold",
        "func": max_area,
        "tests": [(([1, 8, 6, 2, 5, 4, 8, 3, 7],), 49), (([1, 1],), 1)],
        "solution": sol_max_area,
    },
    {
        "id": "4.5",
        "task": "reverse_in_place(arr): swap the ends until the list is flipped",
        "func": reverse_in_place,
        "tests": [(([1, 2, 3],), [3, 2, 1]), (([],), [])],
        "solution": sol_reverse_in_place,
    },
    {
        "id": "4.6",
        "task": "has_pair_with_sum(arr, target): is there a pair that adds up?",
        "func": has_pair_with_sum,
        "tests": [(([1, 2, 4], 6), True), (([1, 2, 3], 100), False)],
        "solution": sol_has_pair_with_sum,
    },
]

DEMOS = [
    ("1. Pair sum in a sorted array", demo_pair_sum_sorted),
    ("2. Palindrome with two pointers", demo_palindrome_two_pointers),
    ("3. Remove duplicates", demo_remove_duplicates),
    ("4. Container with most water", demo_container_most_water),
    ("5. Reverse in place", demo_reverse_in_place),
    ("6. Two pointers vs nested loops", demo_two_pointers_vs_loops),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
