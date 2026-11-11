"""
DSA 13 - Heaps and priority queues
==================================

Today's goal:
  1. Understand what a heap is and what it is good for
  2. Use the heapq module (heappush, heappop, heapify)
  3. Find the k-th largest or k-th smallest value fast
  4. Merge many sorted lists into one sorted list
  5. Keep the running median of a stream of numbers

A heap is a tree that lives inside a list:
  - The SMALLEST value sits at the front (index 0).
  - Every parent is smaller than its children.
  - It is NOT fully sorted - only the front is guaranteed.

Python gives you one for free: the heapq module.
```python
import heapq

heap = []                 # start with an empty list
heapq.heappush(heap, 7)   # add a value
heapq.heappush(heap, 2)
heapq.heappop(heap)       # -> 2, the smallest value
heapq.heapify(numbers)    # turn a list into a heap (changes it in place)
```

Why it is fast:
  heappush and heappop are O(log n) - the log comes from the tree
  getting shorter as you walk down to a leaf, so only log n levels
  have to be touched. heapify is O(n) - it fixes the tree from the
  bottom up, one time, without moving every value all the way.

The classic pattern - keep only the k biggest values:
  Push every value into a heap. When the heap grows bigger than k,
  pop the smallest one out again. At the end the heap holds the k
  biggest values, so heap[0] is the k-th biggest.
  That is O(n log k) - and the log stays small because the heap never
  grows past k.

Two heaps for the running median:
  lower = a MAX heap (store the values negative) with the smaller half
  upper = a MIN heap with the bigger half
  Keep lower the same size as upper, or one value bigger.
  Then the median is right there: the top of lower and the top of upper.

Tip: a heap works with any values that can be compared, not only numbers.
Tip: heapify changes the list in place and returns None.
Tip: if you only need the biggest one or two values, heapq.nlargest
  and heapq.nsmallest do all the work for you.
"""

import heapq

from _dsa_kit import main


# ---------------------------------------------------------------------------
# DEMOS - run these first, then change the code and experiment
# ---------------------------------------------------------------------------


def demo_heapq_basics() -> None:
    # The smallest value of a heap is always at the front.
    numbers = [5, 3, 8, 1, 2]
    heapq.heapify(numbers)
    print("the list      :", [5, 3, 8, 1, 2])
    print("after heapify :", numbers)
    print("heap[0] is the smallest:", numbers[0])
    print("heapify is O(n) - it fixes the whole tree in one go")


def demo_build_min_heap() -> None:
    # Start from any list, turn it into a min heap.
    numbers = [9, 4, 7, 1, -3, 8, 2]
    heap = list(numbers)
    heapq.heapify(heap)
    print("numbers    :", numbers)
    print("as a heap  :", heap)
    print("the heap is not sorted, but the smallest value is at the front")


def demo_heappush_heappop() -> None:
    # Push values in, pop them out - they come out in sorted order.
    heap = []
    for value in [7, 2, 9, 4]:
        heapq.heappush(heap, value)
        print(f"push {value} -> the heap is now {heap}")
    while heap:
        print("pop ->", heapq.heappop(heap))


def demo_kth_largest() -> None:
    # Keep a heap of only the k biggest values.
    # The smallest one inside it is the k-th biggest of the whole list.
    numbers = [3, 2, 1, 5, 6, 4]
    k = 2
    heap = []
    for value in numbers:
        heapq.heappush(heap, value)
        if len(heap) > k:
            heapq.heappop(heap)
    print("numbers :", numbers)
    print("k =", k)
    print("the heap keeps only the", k, "biggest values:", heap)
    print("k-th biggest =", heap[0])
    print("heapq.nlargest(2, numbers) =", heapq.nlargest(2, numbers))


def demo_merge_k_sorted() -> None:
    # heapq.merge takes the smallest head of every list, one by one.
    lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
    print("the lists :", lists)
    print("merged    :", list(heapq.merge(*lists)))
    print("it never sorts everything, it only picks the next value")


def demo_running_median() -> None:
    # Two heaps: the smaller half (stored negative) and the bigger half.
    lower = []      # max heap - we store the values negative
    upper = []      # min heap
    numbers = [5, 15, 1, 3, 8]
    for value in numbers:
        if not lower or value <= -lower[0]:
            heapq.heappush(lower, -value)
        else:
            heapq.heappush(upper, value)
        if len(lower) > len(upper) + 1:
            heapq.heappush(upper, -heapq.heappop(lower))
        elif len(upper) > len(lower):
            heapq.heappush(lower, -heapq.heappop(upper))
        if len(lower) == len(upper):
            median = (-lower[0] + upper[0]) / 2
        else:
            median = -lower[0]
        print(f"after {value:>3} the median is {median}")


# ---------------------------------------------------------------------------
# EXERCISES - write your code where you see TODO
# ---------------------------------------------------------------------------


def kth_largest(nums: list, k: int):
    """Return the k-th largest value of nums, or None if k is too big.

    kth_largest([3, 2, 1, 5, 6, 4], 2) -> 5
    """
    # TODO: keep a heap with only the k biggest values
    return None


def kth_smallest(nums: list, k: int):
    """Return the k-th smallest value of nums, or None if k is too big.

    kth_smallest([3, 2, 1, 5, 6, 4], 2) -> 2
    """
    # TODO: keep a max heap (store the values negative) with the k smallest
    return None


def merge_k_sorted(lists: list) -> list:
    """Return one sorted list made from many sorted lists.

    merge_k_sorted([[1, 4], [2, 3]]) -> [1, 2, 3, 4]
    """
    # TODO: use heapq.merge
    return None


def running_median(nums: list) -> list:
    """Return the median after every number (so one value per number).

    running_median([1, 2, 3]) -> [1, 1.5, 2]
    """
    # TODO: use one max heap for the lower half and one min heap for the upper
    return None


def heap_sort(nums: list) -> list:
    """Return the numbers sorted from small to large using a heap.

    heap_sort([4, 1, 3]) -> [1, 3, 4]
    """
    # TODO: heapify the list, then pop every value out of it
    return None


def min_heap_of_list(nums: list) -> list:
    """Return the list turned into a min heap (the smallest value first).

    min_heap_of_list([4, 1, 3]) -> [1, 4, 3]
    """
    # TODO: copy the list, then heapify the copy
    return None


def count_greater(nums: list, x: int) -> int:
    """Return how many numbers are strictly bigger than x.

    count_greater([1, 2, 3, 2], 2) -> 1
    """
    # TODO: count the numbers that are bigger than x
    return None


# Solutions - try it yourself first, then run with `--solutions`
def sol_kth_largest(nums: list, k: int):
    if k <= 0 or k > len(nums):
        return None
    heap = []
    for value in nums:
        heapq.heappush(heap, value)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]


def sol_kth_smallest(nums: list, k: int):
    if k <= 0 or k > len(nums):
        return None
    heap = []
    for value in nums:
        heapq.heappush(heap, -value)     # max heap, stored negative
        if len(heap) > k:
            heapq.heappop(heap)
    return -heap[0]


def sol_merge_k_sorted(lists: list) -> list:
    return list(heapq.merge(*lists))


def sol_running_median(nums: list) -> list:
    lower = []      # max heap, the values are stored negative
    upper = []      # min heap
    out = []
    for value in nums:
        if not lower or value <= -lower[0]:
            heapq.heappush(lower, -value)
        else:
            heapq.heappush(upper, value)
        if len(lower) > len(upper) + 1:
            heapq.heappush(upper, -heapq.heappop(lower))
        elif len(upper) > len(lower):
            heapq.heappush(lower, -heapq.heappop(upper))
        if len(lower) == len(upper):
            out.append((-lower[0] + upper[0]) / 2)
        else:
            out.append(-lower[0])
    return out


def sol_heap_sort(nums: list) -> list:
    heap = list(nums)
    heapq.heapify(heap)
    out = []
    while heap:
        out.append(heapq.heappop(heap))
    return out


def sol_min_heap_of_list(nums: list) -> list:
    heap = list(nums)
    heapq.heapify(heap)
    return heap


def sol_count_greater(nums: list, x: int) -> int:
    return sum(1 for value in nums if value > x)


EXERCISES = [
    {
        "id": "13.1", "task": "kth_largest(nums, k): the k-th biggest value",
        "func": kth_largest, "tests": [(([3, 2, 1, 5, 6, 4], 2), 5), (([3, 2, 1, 5, 6, 4], 1), 6), (([1, 2], 5), None)],
        "solution": sol_kth_largest,
    },
    {
        "id": "13.2", "task": "kth_smallest(nums, k): the k-th smallest value",
        "func": kth_smallest, "tests": [(([3, 2, 1, 5, 6, 4], 2), 2), (([3, 2, 1, 5, 6, 4], 1), 1), (([1, 2], 3), None)],
        "solution": sol_kth_smallest,
    },
    {
        "id": "13.3", "task": "merge_k_sorted(lists): merge many sorted lists",
        "func": merge_k_sorted, "tests": [(([[1, 4, 5], [1, 3, 4], [2, 6]],), [1, 1, 2, 3, 4, 4, 5, 6]), (([],), [])],
        "solution": sol_merge_k_sorted,
    },
    {
        "id": "13.4", "task": "running_median(nums): the median after every number",
        "func": running_median, "tests": [(([1, 2, 3, 4, 5],), [1, 1.5, 2, 2.5, 3]), (([7],), [7])],
        "solution": sol_running_median,
    },
    {
        "id": "13.5", "task": "heap_sort(nums): sort the numbers with a heap",
        "func": heap_sort, "tests": [(([4, 1, 3, 2],), [1, 2, 3, 4]), (([],), [])],
        "solution": sol_heap_sort,
    },
    {
        "id": "13.6", "task": "min_heap_of_list(nums): the list as a min heap",
        "func": min_heap_of_list, "tests": [(([5, 3, 8, 1, 2],), [1, 2, 8, 3, 5]), (([4, 1, 3],), [1, 4, 3])],
        "solution": sol_min_heap_of_list,
    },
    {
        "id": "13.7", "task": "count_greater(nums, x): how many values are bigger than x",
        "func": count_greater, "tests": [(([1, 2, 3, 2], 2), 1), (([1, 2, 3], 0), 3), (([], 5), 0)],
        "solution": sol_count_greater,
    },
]

DEMOS = [
    ("1. heapq basics", demo_heapq_basics),
    ("2. Build a min heap", demo_build_min_heap),
    ("3. heappush and heappop", demo_heappush_heappop),
    ("4. k-th largest value", demo_kth_largest),
    ("5. Merge k sorted lists", demo_merge_k_sorted),
    ("6. Running median", demo_running_median),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
