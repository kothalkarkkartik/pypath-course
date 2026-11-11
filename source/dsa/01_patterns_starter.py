"""
DSA Starter - 5 classic patterns (just a small taste for now)
=============================================================

Open this file AFTER the Python chapters. Here you only need to see how
the Python you learned is used in DSA.

Run: python dsa/01_patterns_starter.py

Patterns:
  1. Two Sum          -> hashing
  2. Binary Search    -> sorted array
  3. Max Subarray     -> Kadane's algorithm
  4. BFS              -> graph traversal
  5. Fibonacci        -> memoization (the door to DP)
"""

from collections import deque


def two_sum(nums: list, target: int):
    """Return the indexes of two numbers whose sum equals the target. Otherwise None.

    Time: O(n), Space: O(n)
    """
    seen = {}
    for i, n in enumerate(nums):
        need = target - n
        if need in seen:
            return (seen[need], i)
        seen[n] = i
    return None


def binary_search(nums: list, target: int) -> int:
    """Return the index of the target in a sorted list, or -1 if not found.

    Time: O(log n), Space: O(1)
    """
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def max_subarray(nums: list) -> int:
    """The largest contiguous subarray sum (Kadane's algorithm).

    Time: O(n), Space: O(1)
    """
    best = current = nums[0]
    for n in nums[1:]:
        current = max(n, current + n)
        best = max(best, current)
    return best


def bfs(graph: dict, start) -> list:
    """The order of a Breadth First Search.

    Time: O(V + E), Space: O(V)
    """
    visited = {start}
    order = []
    queue = deque([start])

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbour in graph.get(node, []):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)

    return order


def fib(n: int, memo: dict | None = None) -> int:
    """Fibonacci with memoization.

    Time: O(n), Space: O(n)
    """
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n < 2:
        return n
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]


def run_tests() -> None:
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)
    assert two_sum([3, 3], 6) == (0, 1)
    assert two_sum([1, 2], 10) is None

    assert binary_search([1, 3, 5, 7, 9], 7) == 3
    assert binary_search([1, 3, 5], 2) == -1
    assert binary_search([], 1) == -1

    assert max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert max_subarray([1]) == 1
    assert max_subarray([-5, -2, -9]) == -2

    graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D"],
        "D": [],
    }
    assert bfs(graph, "A") == ["A", "B", "C", "D"]

    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(10) == 55
    assert fib(50) == 12586269025

    print("All tests PASS! You just saw how Python connects to DSA.")


def main() -> None:
    print("=" * 56)
    print("DSA STARTER - 5 patterns")
    print("=" * 56)

    nums = [2, 7, 11, 15]
    print(f"\n1. two_sum({nums}, 9) = {two_sum(nums, 9)}")

    sorted_nums = [1, 3, 5, 7, 9]
    print(f"2. binary_search({sorted_nums}, 7) = {binary_search(sorted_nums, 7)}")

    arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"3. max_subarray({arr}) = {max_subarray(arr)}")

    graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
    print(f"4. bfs(graph, 'A') = {bfs(graph, 'A')}")

    print(f"5. fib(50) = {fib(50)}")

    print()
    run_tests()
    print("\nNext: read dsa/00_roadmap.md (after you finish Python).")


if __name__ == "__main__":
    main()
