# DSA Roadmap (with Python) - 12 Weeks

> **The chapters are ready:** `dsa/d01_patterns.py` to `dsa/d16_binary_search_answers.py`
> are 16 full chapters with notes, runnable demos and auto-tested exercises.
> Start with `dsa/d01_patterns.py` (or open the **DSA** section in the portal).
>
> **Before this:** complete `chapters/00` to `16` + build the 3 projects.
> The foundation of DSA = a good understanding of loops, lists, dicts, sets, functions and recursion.
> Memorising DSA without a Python base won't get you anywhere.

### Which chapter for which week

| Week | Topic | Chapter file |
|------|-------|--------------|
| 1 | Arrays, strings, two pointers | `d02_arrays.py`, `d03_strings.py`, `d04_two_pointers.py` |
| 2 | Hashing | `d07_hashing.py` |
| 3 | Stacks, queues, deque | `d08_stacks.py`, `d09_queues.py` |
| 4 | Linked lists | `d10_linked_list.py` |
| 5 | Recursion + backtracking | `d11_recursion.py` |
| 6 | Sorting + binary search | `d06_sorting_searching.py`, `d16_binary_search_answers.py` |
| 7 | Trees + BST | `d12_trees.py` |
| 8 | Heaps + priority queue | `d13_heaps.py` |
| 9 | Graphs | `d14_graphs.py` |
| 10 | Dynamic programming | `d15_dynamic_programming.py` |
| 11 | Sliding window + patterns | `d05_sliding_window.py`, `d01_patterns.py` |
| 12 | Revision + mocks | all of the above |

---

## Week-wise plan

| Week | Topic | What to practice | Target problems |
|------|-------|------------------|-----------------|
| 1 | Arrays, strings, two pointers | Reverse, palindrome, pair sum, max subarray | 10 |
| 2 | Hashing | Two sum, frequency, anagram, subarray sum = k | 10 |
| 3 | Stacks, queues, deque | Valid brackets, next greater, sliding window max | 8 |
| 4 | Linked lists | Reverse, middle, cycle, merge two lists | 8 |
| 5 | Recursion + backtracking | Subsets, permutations, N-queens | 10 |
| 6 | Sorting + binary search | Merge sort, quick sort, search space problems | 10 |
| 7 | Trees + BST | Traversals, height, LCA, validate BST | 10 |
| 8 | Heaps + priority queue | Kth largest, top K frequent, merge K lists | 8 |
| 9 | Graphs | BFS, DFS, islands, topological sort | 10 |
| 10 | Dynamic programming | Climbing stairs, knapsack, LIS, coin change | 12 |
| 11 | Greedy + bits | Intervals, jump game, XOR tricks | 8 |
| 12 | Revision + mocks | Random mix, timed contests, weak topics | 10 |

Total: ~110 problems. Two problems a day = done in 8 weeks, so the 12-week plan has some buffer.

---

## Daily DSA routine (60-90 min)

1. **10 min** - rewrite the code for one problem from yesterday (without looking).
2. **10 min** - read a new problem, think of the brute force, write down the complexity.
3. **25 min** - solve it yourself. If you're stuck after 25 min, look at a hint, then still write the code yourself.
4. **15 min** - look at the solution, understand the better approach, and note it in your own words.
5. **10 min** - one more problem using the same pattern.

**Golden rule:** after you solve a problem, **close the code and write it again**. This is what actually helps in interviews.

---

## Problem-solving framework (for every question)

1. Write the **input/output** clearly. Take an example.
2. State the **brute force** (with its time/space).
3. Spot the **pattern**: sorted? duplicates? subarray? shortest path? choices?
4. Think of a **better approach**. Try changing the data structure.
5. **Edge cases:** empty, 1 element, negative, duplicates, overflow.
6. Write the **complexity**: time + space.
7. Write the **code**, then do a dry run.

---

## Python DSA templates

### Fast input (competitive)

```python
import sys
input = sys.stdin.readline

n = int(input())
nums = list(map(int, input().split()))
```

### Array / two pointers

```python
left, right = 0, len(nums) - 1
while left < right:
    # logic
    left += 1
    right -= 1
```

### Frequency map

```python
from collections import Counter, defaultdict

count = Counter(nums)
groups = defaultdict(list)
```

### Stack

```python
stack = []
stack.append(x)
top = stack[-1]
stack.pop()
```

### Queue / BFS

```python
from collections import deque

q = deque([start])
visited = {start}
while q:
    node = q.popleft()
    for nei in graph[node]:
        if nei not in visited:
            visited.add(nei)
            q.append(nei)
```

### Heap

```python
import heapq

heap = []
heapq.heappush(heap, x)
smallest = heapq.heappop(heap)
heapq.heapify(nums)                 # turn a list into a heap
largest = heapq.nlargest(3, nums)
```

### Binary search

```python
lo, hi = 0, len(nums) - 1
while lo <= hi:
    mid = (lo + hi) // 2
    if nums[mid] == target:
        return mid
    if nums[mid] < target:
        lo = mid + 1
    else:
        hi = mid - 1
```

### Recursion / backtracking

```python
def backtrack(path, options, result):
    if done(path):
        result.append(path.copy())
        return
    for option in options:
        if valid(option):
            path.append(option)
            backtrack(path, next_options, result)
            path.pop()          # undo
```

### Memoization

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def dp(i, j):
    ...
```

### Graph build

```python
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)      # undirected
```

### Sorting with a custom key

```python
intervals.sort(key=lambda x: x[0])          # start time
people.sort(key=lambda p: (-p[1], p[0]))    # desc, then asc
```

---

## Important patterns (remember the names)

| Pattern | When to use it |
|---------|----------------|
| Two pointers | Sorted array, pair sum, palindrome |
| Sliding window | Subarray/substring with a condition |
| Prefix sum | Range sum, subarray sum = k |
| Hashing | Duplicates, frequency, lookup |
| Fast/slow pointers | Linked list cycle, middle |
| Binary search on the answer | Min/max possible value |
| Monotonic stack | Next greater/smaller element |
| BFS | Shortest path (unweighted), levels |
| DFS/backtracking | All paths, combinations, islands |
| Heap / top K | Kth largest, merge K sorted |
| DP (1D/2D) | Choices + overlapping subproblems |
| Greedy | Local best = global best (intervals) |
| Union-Find | Connected components, cycle detection |
| Trie | Prefix search, autocomplete |

---

## Resources

- **NeetCode 150** - a pattern-wise curated list (the best starting point)
- **LeetCode** - daily practice + contests
- **CSES Problem Set** - solid for the fundamentals
- **Python docs** - `collections`, `heapq`, `bisect`, `itertools`

**Solving problems yourself** matters more than courses or YouTube. Watching videos = passive, problem solving = active.

---

## After DSA

- SQL basics
- OS + DBMS + CN (interview theory)
- 2-3 solid projects (API + database + frontend)
- Resume + mock interviews

---

## What to do right now

1. Run `python practice.py`.
2. Start from Chapter 1.
3. One chapter a day + a 10-minute quiz.
4. Come back here after 20 days.

When you finish Python, tell me: **"Build the DSA chapters"** - I'll create chapter-wise DSA files in the same style (from arrays to DP), with tests and solutions.
