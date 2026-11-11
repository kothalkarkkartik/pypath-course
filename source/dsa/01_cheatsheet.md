# DSA Cheatsheet (Python) - the templates you will use again and again

> Copy any template into a file, change the names, and solve the problem.
> Every template below is short on purpose.

---

## 1. The problem-solving frame (use it every time)

```python
# 1. input / output written clearly
# 2. brute force first (even if slow)
# 3. spot the pattern
# 4. better idea
# 5. edge cases: empty, one item, duplicates, negative
# 6. write the complexity
```

**Complexity cheat sheet**

| Name | Meaning | Example |
|------|---------|---------|
| O(1) | instant | `arr[0]`, `dict[key]` |
| O(log n) | halves each time | binary search |
| O(n) | one pass | sum of a list |
| O(n log n) | one pass + log work per item | `sorted()`, merge sort |
| O(n²) | nested loops | pair sum by brute force |
| O(2ⁿ) | every subset | brute-force subsets |

---

## 2. Two pointers (sorted array)

```python
def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        total = arr[left] + arr[right]
        if total == target:
            return left, right
        if total < target:
            left += 1
        else:
            right -= 1
    return None
```

---

## 3. Sliding window (fixed size)

```python
def max_sum_k(arr, k):
    if not arr or k > len(arr):
        return 0
    window = sum(arr[:k])
    best = window
    for i in range(k, len(arr)):
        window += arr[i] - arr[i - k]
        best = max(best, window)
    return best
```

## 3b. Sliding window (variable size)

```python
def longest_unique(s):
    seen = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        seen[ch] = right
        while left in seen and s[left] in s[seen[ch]:seen[ch]]:
            left += 1
        best = max(best, right - left + 1)
    return best
```

---

## 4. Binary search

```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

**Lower bound (first index >= target)**

```python
def lower_bound(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

---

## 5. Hashing (dict / set)

```python
# two sum in O(n)
def two_sum(arr, target):
    seen = {}
    for i, value in enumerate(arr):
        if target - value in seen:
            return seen[target - value], i
        seen[value] = i
    return None
```

```python
# count items
counts = {}
for item in items:
    counts[item] = counts.get(item, 0) + 1
```

---

## 6. Stack

```python
stack = []
stack.append(x)     # push
stack.pop()         # pop
stack[-1]           # peek
```

**Valid parentheses**

```python
def is_valid(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif not stack or stack.pop() != pairs[ch]:
            return False
    return not stack
```

---

## 7. Queue / BFS

```python
from collections import deque

queue = deque([start])
seen = {start}
while queue:
    node = queue.popleft()
    for nxt in graph[node]:
        if nxt not in seen:
            seen.add(nxt)
            queue.append(nxt)
```

---

## 8. Linked list

```python
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next
```

**Reverse**

```python
def reverse_list(head):
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next
    return prev
```

**Cycle detection (Floyd)**

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
```

---

## 9. Recursion and backtracking

```python
def subsets(nums):
    result = []
    def backtrack(start, current):
        result.append(current[:])
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()
    backtrack(0, [])
    return result
```

**Grid paths**

```python
def count_paths(grid):
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = 1
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                continue
            if r > 0:
                dp[r][c] += dp[r - 1][c]
            if c > 0:
                dp[r][c] += dp[r][c - 1]
    return dp[-1][-1]
```

---

## 10. Trees

```python
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
```

**DFS**

```python
def inorder(node, out=None):
    out = [] if out is None else out
    if node:
        inorder(node.left, out)
        out.append(node.value)
        inorder(node.right, out)
    return out
```

**BFS / level order**

```python
from collections import deque

def level_order(root):
    if not root:
        return []
    out, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.value)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        out.append(level)
    return out
```

---

## 11. Heap

```python
import heapq

heap = []
heapq.heappush(heap, 5)
heapq.heappop(heap)      # smallest
heapq.heapify(items)     # items becomes a heap
```

---

## 12. Graphs

```python
# BFS - shortest path in an unweighted graph
def shortest_path(graph, start, target):
    from collections import deque
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        node, steps = queue.popleft()
        if node == target:
            return steps
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, steps + 1))
    return -1
```

```python
# Topological sort (needs a DAG)
from collections import deque, defaultdict

def topological_order(graph):
    indegree = {node: 0 for node in graph}
    for neighbours in graph.values():
        for nxt in neighbours:
            indegree[nxt] += 1
    queue = deque([n for n, d in indegree.items() if d == 0])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return order if len(order) == len(graph) else []
```

---

## 13. Dynamic programming

**Memoised recursion**

```python
def fib(n, memo=None):
    memo = {} if memo is None else memo
    if n < 2:
        return n
    if n in memo:
        return memo[n]
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]
```

**Bottom-up table**

```python
def climb_stairs(n):
    ways = [1] * (n + 1)
    for i in range(2, n + 1):
        ways[i] = ways[i - 1] + ways[i - 2]
    return ways[n]
```

**0/1 Knapsack**

```python
def max_knapsack(weights, values, capacity):
    best = [0] * (capacity + 1)
    for weight, value in zip(weights, values):
        for cap in range(capacity, weight - 1, -1):
            best[cap] = max(best[cap], best[cap - weight] + value)
    return best[capacity]
```

---

## 14. Sorting in Python

```python
sorted(nums)                 # new list
nums.sort()                   # in place
nums.sort(key=lambda x: -x)  # custom order
nums.sort(key=lambda x: x[1])
```

**Merge two sorted lists**

```python
def merge(a, b):
    out = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    out.extend(a[i:]); out.extend(b[j:])
    return out
```

---

## 15. The 10 patterns that cover most questions

1. Two pointers on a **sorted** array
2. Sliding window (fixed or variable size)
3. Binary search on a **sorted** array
4. Binary search on the **answer**
5. Hashing with a dict or set
6. Stack for brackets and next-greater
7. BFS/DFS on a grid
8. BFS/DFS on a graph
9. Topological sort on a DAG
10. DP on a 1D or 2D array

If you recognise the pattern, half the solution is already written.
