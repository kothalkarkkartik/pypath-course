"""
DSA 16 - Binary search on the answer
====================================

Today's goal:
  1. Learn to binary search over a range of possible answers
  2. Use it for the square root, shipping, cows and rotated arrays
  3. Find the first position where a condition becomes true

Normal binary search looks for a value inside a sorted list.
Binary search on the answer is a bit different. Instead of searching
a list, we search a space of possible answers:
  "What is the smallest capacity that works?"
  "What is the biggest distance that works?"

We guess an answer in the middle and ask a yes/no question:
  - If the answer works, maybe a bigger one works too -> search right.
  - If it does not work, every bigger one fails as well -> search left.

This works only when the question is monotonic: once something is
possible it stays possible (or once something is impossible it stays
impossible). That is why the middle guess always makes sense.

The skeleton:
```python
lo, hi = smallest_possible, biggest_possible
while lo < hi:
    mid = (lo + hi) // 2
    if possible(mid):
        hi = mid          # mid works, try to find a smaller one
    else:
        lo = mid + 1      # mid fails, we need something bigger
return lo
```

Integer square root:
  We look for the biggest r with r * r <= x. "r * r is still small
  enough" stays true for small r, so the search works.
Shipping packages:
  "Can I ship everything in D days with capacity C?" is easy to check -
  load packages in order until the day is full. If C works, C + 1 works
  too -> monotonic -> binary search.
Cows in stalls:
  "Can I place C cows at least D apart?" - place the first cow in the
  first stall and always put the next cow in the earliest stall that is
  far enough away. If D works, D + 1 may not -> search the biggest D.
Rotated sorted array:
  A sorted array that was cut in half and the two halves swapped. One
  of the two halves is still sorted, so we can decide where to go.

Complexity in simple words:
  Binary search on the answer is O(log R) - we cut the search space in
  half every time, so even 1 000 000 000 answers need only 30 steps.

Tip: before you code, write down two things:
  1. the range of possible answers (lo and hi)
  2. the yes/no check function
  Without a check function, binary search cannot help.
"""

from _dsa_kit import main


def _days_needed(weights: list, capacity: int) -> int:
    days, used = 1, 0
    for weight in weights:
        if used + weight > capacity:
            days, used = days + 1, 0
        used += weight
    return days


def _can_place(places: list, cows: int, distance: int) -> bool:
    """Can we put `cows` cows in the stalls at least `distance` apart?"""
    count, last = 1, places[0]
    for place in places[1:]:
        if place - last >= distance:
            count, last = count + 1, place
            if count >= cows:
                return True
    return False


# ---------------------------------------------------------------------------
# DEMOS - run these first, then change the code and experiment
# ---------------------------------------------------------------------------


def demo_integer_sqrt() -> None:
    # Find the biggest r with r * r <= x.
    x = 30
    lo, hi = 0, x + 1
    while lo < hi:
        mid = (lo + hi) // 2
        print(f"   guess {mid}: {mid} * {mid} = {mid * mid} (x = {x})")
        if mid * mid <= x:
            lo = mid + 1          # this guess works, look for a bigger one
        else:
            hi = mid              # too big, come down
    print("floor square root of", x, "=", lo - 1)


def demo_ship_days() -> None:
    # Smallest capacity per day that ships every package in D days.
    weights = [1, 2, 3, 4, 5, 6]
    days = 3
    low, high = max(weights), sum(weights)
    while low < high:
        mid = (low + high) // 2
        needed = _days_needed(weights, mid)
        print(f"   capacity {mid} -> needs {needed} days (we have {days})")
        if needed <= days:
            high = mid            # it fits, maybe a smaller one fits too
        else:
            low = mid + 1
    print("minimum capacity:", low)


def demo_cow_distances() -> None:
    # The smallest gap we can keep, and the biggest one we can keep.
    stalls = [1, 2, 4, 8, 9]
    cows = 3
    places = sorted(stalls)
    gaps = [places[i + 1] - places[i] for i in range(len(places) - 1)]
    print("stalls:", places, "gaps:", gaps, "smallest gap:", min(gaps))
    low, high = 0, places[-1] - places[0]
    while low < high:
        mid = (low + high + 1) // 2
        fits = _can_place(places, cows, mid)
        print(f"   distance {mid} -> {'fits' if fits else 'too big'}")
        if fits:
            low = mid             # it fits, try an even bigger distance
        else:
            high = mid - 1
    print("best distance:", low)


def demo_search_rotated() -> None:
    # A sorted array that was cut and swapped, like [4,5,6,7,0,1,2].
    arr = [4, 5, 6, 7, 0, 1, 2]
    target = 0
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            print(f"   found {target} at index {mid}")
            break
        if arr[lo] <= arr[mid]:
            print(f"   mid={mid} value={arr[mid]} -> left half is sorted")
            if arr[lo] <= target < arr[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            print(f"   mid={mid} value={arr[mid]} -> right half is sorted")
            if arr[mid] < target <= arr[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    else:
        print(f"   {target} is not in the array")


def demo_first_true_index() -> None:
    # The array is 0,0,0,1,1,1 - find where the first 1 is.
    arr = [0, 0, 0, 1, 1, 1]
    lo, hi, answer = 0, len(arr) - 1, -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == 1:
            answer = mid
            hi = mid - 1        # the first 1 can only be further left
        else:
            lo = mid + 1
    print("array:", arr)
    print("first 1 is at index:", answer)


# ---------------------------------------------------------------------------
# EXERCISES - write your code where you see TODO
# ---------------------------------------------------------------------------


def my_sqrt(x: int) -> int:
    """The largest integer r with r * r <= x (the floor of the square root).
    my_sqrt(30) -> 5
    """
    # TODO: binary search between 0 and x
    return None

def ship_days(weights: list, days: int) -> int:
    """Smallest per-day capacity that ships every package within `days` days.
    Packages keep their order and cannot be split. Return -1 if impossible.
    ship_days([1, 2, 3, 4, 5, 6], 3) -> 9
    """
    # TODO: binary search the capacity and check it with a small loop
    return None

def min_distance(stalls: list, cows: int) -> int:
    """Smallest distance you can keep between two cows, or -1 if impossible.
    min_distance([1, 3, 7], 2) -> 2
    """
    # TODO: sort the stalls and look at the gaps between them
    return None

def max_distance(stalls: list, cows: int) -> int:
    """Biggest distance you can keep between every pair of cows.
    max_distance([1, 2, 4, 8, 9], 3) -> 3
    """
    # TODO: binary search the distance and check it greedily
    return None

def search_rotated(arr: list, target) -> int:
    """Index of target in a rotated sorted array, or -1 when it is missing.
    search_rotated([4, 5, 6, 7, 0, 1, 2], 0) -> 4
    """
    # TODO: find the sorted half on every step and shrink the search
    return None

def first_true_index(arr: list) -> int:
    """Index of the first 1 in an array of 0s followed by 1s, or -1.
    first_true_index([0, 0, 1, 1]) -> 2
    """
    # TODO: binary search for the first 1
    return None

def sqrt_with_binary_search(x: int) -> int:
    """Floor of the square root, found by searching for the first too-big r.
    sqrt_with_binary_search(30) -> 5
    """
    # TODO: find the smallest r with r * r > x and return r - 1
    return None


# Solutions - try it yourself first, then run with `--solutions`
def sol_my_sqrt(x: int) -> int:
    if x <= 0:
        return 0
    if x < 4:
        return x
    lo, hi = 1, x // 2
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid * mid <= x:
            lo = mid + 1
        else:
            hi = mid - 1
    return hi

def sol_ship_days(weights: list, days: int) -> int:
    if days < 1:
        return -1
    if not weights:
        return 0
    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if _days_needed(weights, mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo

def sol_min_distance(stalls: list, cows: int) -> int:
    if cows < 2 or cows > len(stalls):
        return -1
    places = sorted(stalls)
    gaps = [places[i + 1] - places[i] for i in range(len(places) - 1)]
    return min(gaps)

def sol_max_distance(stalls: list, cows: int) -> int:
    if cows < 2 or cows > len(stalls):
        return -1
    places = sorted(stalls)
    lo, hi = 0, places[-1] - places[0]
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if _can_place(places, cows, mid):
            lo = mid
        else:
            hi = mid - 1
    return lo

def sol_search_rotated(arr: list, target) -> int:
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[lo] <= arr[mid]:
            if arr[lo] <= target < arr[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if arr[mid] < target <= arr[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1

def sol_first_true_index(arr: list) -> int:
    lo, hi, answer = 0, len(arr) - 1, -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == 1:
            answer = mid
            hi = mid - 1       # look further to the left
        else:
            lo = mid + 1
    return answer

def sol_sqrt_with_binary_search(x: int) -> int:
    if x <= 0:
        return 0
    lo, hi = 0, x + 1
    while lo < hi:
        mid = (lo + hi) // 2
        if mid * mid <= x:
            lo = mid + 1
        else:
            hi = mid
    return lo - 1


EXERCISES = [
    {
        "id": "16.1", "task": "my_sqrt(x): the floor of the square root of x",
        "func": my_sqrt,
        "tests": [((0,), 0), ((1,), 1), ((8,), 2), ((9,), 3), ((16,), 4), ((15,), 3)],
        "solution": sol_my_sqrt,
    },
    {
        "id": "16.2", "task": "ship_days(weights, days): smallest per-day capacity, or -1",
        "func": ship_days,
        "tests": [(([1, 2, 3, 4, 5, 6], 3), 9), (([1, 2, 3], 1), 6), (([10], 1), 10), (([1, 2], 0), -1)],
        "solution": sol_ship_days,
    },
    {
        "id": "16.3", "task": "min_distance(stalls, cows): smallest gap between two cows",
        "func": min_distance,
        "tests": [(([1, 3, 7], 2), 2), (([1, 2, 4, 8, 9], 3), 1), (([1, 2, 3], 3), 1), (([1, 2, 3], 4), -1)],
        "solution": sol_min_distance,
    },
    {
        "id": "16.4", "task": "max_distance(stalls, cows): biggest gap between every pair",
        "func": max_distance,
        "tests": [(([1, 2, 4, 8, 9], 3), 3), (([1, 2, 3, 4, 5], 3), 2), (([1, 2], 2), 1), (([1, 2], 5), -1)],
        "solution": sol_max_distance,
    },
    {
        "id": "16.5", "task": "search_rotated(arr, target): index in a rotated sorted array",
        "func": search_rotated,
        "tests": [(([4, 5, 6, 7, 0, 1, 2], 0), 4), (([4, 5, 6, 7, 0, 1, 2], 5), 1), (([4, 5, 6, 7, 0, 1, 2], 3), -1), (([1], 1), 0)],
        "solution": sol_search_rotated,
    },
    {
        "id": "16.6", "task": "first_true_index(arr): index of the first 1, or -1",
        "func": first_true_index,
        "tests": [(([0, 0, 0, 1, 1],), 3), (([1, 1],), 0), (([0, 0],), -1), (([],), -1)],
        "solution": sol_first_true_index,
    },
    {
        "id": "16.7", "task": "sqrt_with_binary_search(x): the floor of the square root",
        "func": sqrt_with_binary_search,
        "tests": [((0,), 0), ((1,), 1), ((25,), 5), ((99,), 9), ((100,), 10)],
        "solution": sol_sqrt_with_binary_search,
    },
]

DEMOS = [
    ("1. Integer square root", demo_integer_sqrt),
    ("2. Shipping capacity in days", demo_ship_days),
    ("3. Cow distances: smallest and biggest gap", demo_cow_distances),
    ("4. Search in a rotated array", demo_search_rotated),
    ("5. First position where a condition is true", demo_first_true_index),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
