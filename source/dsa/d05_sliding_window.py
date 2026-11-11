"""
DSA 05 - Sliding window
========================

Today's goal:
  1. See the sliding window idea: keep a window and move it one step
  2. Use a fixed size window (always the same number of items)
  3. Use a variable size window (it grows and shrinks as needed)
  4. Meet Kadane's algorithm, the most famous window of all

The problem it solves: many questions ask about "every group of k
  neighbours" or "the longest piece without a repeat". Checking every
  group from scratch means doing the same work again and again.

The slow way (brute force):
```python
for start in range(len(arr) - k + 1):
    total = sum(arr[start:start + k])   # k steps, for every start
```
  That is O(n * k): for 100 numbers and a window of 10 we add 1000 times.

The fast way (sliding window):
  Keep the total of the current window. When the window moves one step
  to the right, one number leaves and one number arrives:
```python
total = total - arr[left] + arr[right]
```
  Now every number is touched only a couple of times, so the whole scan
  is O(n) - one pass.

Two kinds of window:
  - Fixed size: the window always holds exactly k items (fixed window sum).
  - Variable size: it grows on the right and shrinks on the left when
    the condition breaks (longest unique substring).

Kadane's algorithm is a tiny special case: the window is "the best sum
ending here", so we extend that run or start a fresh one.

Why it works:
  - Fixed window: the total is always the sum of the items inside it.
  - Variable window: `left` only moves forward, so no item is used
    twice and no item is skipped.

Speed: the fixed window sum is O(n) - one pass over the list. The longest
unique substring is also O(n) - each letter enters and leaves once.

Tips:
  - Fixed size? Use "add the new one, remove the old one".
  - Flexible size? Use "extend right, shrink left while it is broken".
"""

from _dsa_kit import main


# ---------------------------------------------------------------------------
# DEMOS - run these first, then change the code and experiment
# ---------------------------------------------------------------------------


def demo_kadane_max_subarray() -> None:
    # Kadane: the biggest sum we can get from one chunk of neighbours.
    arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    best = current = arr[0]
    for value in arr[1:]:
        current = max(value, current + value)   # extend the run or start fresh
        best = max(best, current)
    print("array:", arr, "-> best sum:", best, "(the chunk 4, -1, 2, 1)")


def demo_fixed_window_sum() -> None:
    # A window of exactly 3 numbers that slides across the whole list.
    arr = [2, 1, 5, 1, 3, 2]
    k = 3
    total = sum(arr[:k])            # the first window, we add it up once
    print("array:", arr, "window size:", k, "- window 1:", arr[:k], "sum =", total)
    for right in range(k, len(arr)):
        total = total - arr[right - k] + arr[right]   # slide one step
        print("window", right - k + 2, ":", arr[right - k + 1:right + 1], "sum =", total)


def demo_longest_unique_substring() -> None:
    # The window must not contain the same letter twice.
    s = "abcabcbb"
    last_seen = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1     # jump past the old copy
        last_seen[ch] = right
        best = max(best, right - left + 1)
    print("string:", s, "-> longest part without repeats:", best, "letters")


def demo_min_subarray_of_size_k() -> None:
    # The smallest sum we can get from exactly k neighbours.
    arr = [4, 2, 1, 3]
    k = 2
    total = sum(arr[:k])
    smallest = total
    for right in range(k, len(arr)):
        total = total - arr[right - k] + arr[right]
        smallest = min(smallest, total)
    print("array:", arr, "size:", k, "-> smallest window sum:", smallest)


def demo_anagram_window() -> None:
    # Every place where the pattern shows up with its letters shuffled.
    text = "abcbad"
    pattern = "abc"
    need = {ch: pattern.count(ch) for ch in pattern}
    window = {}
    left = 0
    hits = []
    for right, ch in enumerate(text):
        window[ch] = window.get(ch, 0) + 1
        while window[ch] > need.get(ch, 0):       # too many of this letter
            window[text[left]] -= 1               # drop from the left
            left += 1
        if right - left + 1 == len(pattern):
            if all(window.get(c, 0) == n for c, n in need.items()):
                hits.append(left)
            window[text[left]] -= 1
            left += 1
    print("text:", text, "pattern:", pattern, "-> anagram windows at:", hits)


# ---------------------------------------------------------------------------
# EXERCISES - write your code where you see TODO
# ---------------------------------------------------------------------------


def max_subarray_sum(arr: list) -> int:
    """Return the biggest sum of any chunk of neighbours (0 for an empty list).

    max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]) -> 6
    """
    # TODO: use Kadane's algorithm - one pass over the list
    return None


def fixed_window_sum(arr: list, k: int) -> int:
    """Return the sum of the first window of exactly k numbers (None if it does not fit).

    fixed_window_sum([1, 2, 3, 4, 5], 3) -> 6
    """
    # TODO: take only the first k numbers and add them up
    return None


def longest_unique_substring(s: str) -> int:
    """Return the length of the longest part of s where no letter repeats.

    longest_unique_substring("abcabcbb") -> 3
    """
    # TODO: use a window and remember the last spot of each letter
    return None


def min_subarray_sum(arr: list, k: int) -> int:
    """Return the smallest sum of exactly k neighbours (0 if the list is too short).

    min_subarray_sum([4, 2, 1, 3], 2) -> 3
    """
    # TODO: slide a window of size k over the list
    return None


def longest_substring_k_distinct(s: str, k: int) -> int:
    """Return the length of the longest part of s with at most k different letters.

    longest_substring_k_distinct("eceba", 2) -> 3
    """
    # TODO: grow the window to the right, shrink it from the left
    return None


def max_sum_k_subarray(arr: list, k: int) -> int:
    """Return the biggest sum of exactly k neighbours (0 if the list is too short).

    max_sum_k_subarray([2, 1, 5, 1, 3, 2], 3) -> 9
    """
    # TODO: slide a window of size k over the list
    return None


def window_average(arr: list, k: int) -> list:
    """Return the average of every window of size k (an empty list if it does not fit).

    window_average([1, 2, 3, 4, 5], 3) -> [2.0, 3.0, 4.0]
    """
    # TODO: slide a window of size k and keep the total
    return None


# Solutions - try it yourself first, then run with `--solutions`
def sol_max_subarray_sum(arr: list) -> int:
    if not arr:
        return 0
    best = current = arr[0]
    for value in arr[1:]:
        current = max(value, current + value)
        best = max(best, current)
    return best


def sol_fixed_window_sum(arr: list, k: int) -> int:
    if k <= 0 or k > len(arr):
        return None
    return sum(arr[:k])


def sol_longest_unique_substring(s: str) -> int:
    last_seen = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best


def sol_min_subarray_sum(arr: list, k: int) -> int:
    if k <= 0 or k > len(arr):
        return 0
    total = sum(arr[:k])
    smallest = total
    for right in range(k, len(arr)):
        total = total - arr[right - k] + arr[right]
        smallest = min(smallest, total)
    return smallest


def sol_longest_substring_k_distinct(s: str, k: int) -> int:
    if k <= 0:
        return 0
    counts = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        counts[ch] = counts.get(ch, 0) + 1
        while len(counts) > k:
            first = s[left]
            counts[first] -= 1
            if counts[first] == 0:
                del counts[first]
            left += 1
        best = max(best, right - left + 1)
    return best


def sol_max_sum_k_subarray(arr: list, k: int) -> int:
    if k <= 0 or k > len(arr):
        return 0
    total = sum(arr[:k])
    biggest = total
    for right in range(k, len(arr)):
        total = total - arr[right - k] + arr[right]
        biggest = max(biggest, total)
    return biggest


def sol_window_average(arr: list, k: int) -> list:
    if k <= 0 or k > len(arr):
        return []
    total = sum(arr[:k])
    averages = [total / k]
    for right in range(k, len(arr)):
        total = total - arr[right - k] + arr[right]
        averages.append(total / k)
    return averages


EXERCISES = [
    {
        "id": "5.1",
        "task": "max_subarray_sum(arr): biggest sum of a chunk of neighbours",
        "func": max_subarray_sum,
        "tests": [(([-2, 1, -3, 4, -1, 2, 1, -5, 4],), 6), (([1, 2, 3],), 6), (([-5, -2, -9],), -2)],
        "solution": sol_max_subarray_sum,
    },
    {
        "id": "5.2",
        "task": "fixed_window_sum(arr, k): sum of the first window of k numbers",
        "func": fixed_window_sum,
        "tests": [(([1, 2, 3, 4, 5], 3), 6), (([10, 20], 2), 30), (([1, 2, 3], 5), None)],
        "solution": sol_fixed_window_sum,
    },
    {
        "id": "5.3",
        "task": "longest_unique_substring(s): longest part with no repeated letter",
        "func": longest_unique_substring,
        "tests": [(("abcabcbb",), 3), (("bbbb",), 1), (("",), 0)],
        "solution": sol_longest_unique_substring,
    },
    {
        "id": "5.4",
        "task": "min_subarray_sum(arr, k): smallest sum of exactly k neighbours",
        "func": min_subarray_sum,
        "tests": [(([4, 2, 1, 3], 2), 3), (([1, 2, 3], 3), 6), (([5], 2), 0)],
        "solution": sol_min_subarray_sum,
    },
    {
        "id": "5.5",
        "task": "longest_substring_k_distinct(s, k): longest part with at most k letters",
        "func": longest_substring_k_distinct,
        "tests": [(("eceba", 2), 3), (("abcde", 2), 2), (("a", 0), 0)],
        "solution": sol_longest_substring_k_distinct,
    },
    {
        "id": "5.6",
        "task": "max_sum_k_subarray(arr, k): biggest sum of exactly k neighbours",
        "func": max_sum_k_subarray,
        "tests": [(([2, 1, 5, 1, 3, 2], 3), 9), (([4, -1, 3, -2], 2), 3), (([1], 2), 0)],
        "solution": sol_max_sum_k_subarray,
    },
    {
        "id": "5.7",
        "task": "window_average(arr, k): average of every window of size k",
        "func": window_average,
        "tests": [(([1, 2, 3, 4, 5], 3), [2.0, 3.0, 4.0]), (([2, 4, 6], 2), [3.0, 5.0]), (([1, 2], 3), [])],
        "solution": sol_window_average,
    },
]

DEMOS = [
    ("1. Kadane - max subarray sum", demo_kadane_max_subarray),
    ("2. Fixed size window sum", demo_fixed_window_sum),
    ("3. Longest substring with unique characters", demo_longest_unique_substring),
    ("4. Minimum subarray of size k", demo_min_subarray_of_size_k),
    ("5. Anagram window", demo_anagram_window),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
