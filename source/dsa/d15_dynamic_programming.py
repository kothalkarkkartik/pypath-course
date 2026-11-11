"""
DSA 15 - Dynamic programming
============================

Today's goal:
  1. See what makes a problem a dynamic programming (DP) problem
  2. Use a table (or a memo) to remember answers we already computed
  3. Solve the classic set: stairs, coins, LIS, grid paths, knapsack, robber

What is dynamic programming?
  A DP problem has two special features:
    1. The big problem can be split into smaller versions of itself.
    2. The same small problem shows up again and again.
  When that happens, doing the work twice is wasteful. So we save the
  answer the first time and reuse it later.

Two ways to save the answers:
  Bottom up (a table): we build the answers from the smallest problem to
  the biggest one. Best when the answers are simple numbers.
  Top down (memoisation): we use recursion and a dict that remembers
  what we already computed. Best when the state has many parts.

Memoisation looks like this:
```python
memo = {0: 0, 1: 1}

def fib(n):
    if n in memo:          # we know this one already
        return memo[n]
    memo[n] = fib(n - 1) + fib(n - 2)
    return memo[n]
```

Plain recursion for fib does the same work again and again: for fib(20)
it calls the function more than 20 000 times. With the memo it needs
about 20 calls, because every result is saved and looked up instead of
being calculated a second time.

Every DP solution has three parts:
  1. State    - what is one cell of the table? (fib(n), dp[row][col])
  2. Choice   - what can I do from here? (take the coin or do not)
  3. Base case - what is the answer for the smallest problem?

The classic examples in this chapter:
  Climbing stairs  - ways[i] = ways[i-1] + ways[i-2]
  Coin change      - best[value] = best[value - coin] + 1
  LIS              - best[i] = longest increasing sequence ending at i
  Grid paths       - dp[r][c] = dp[r-1][c] + dp[r][c-1]
  Knapsack         - best[c] = max(best[c], best[c - weight] + value)
  House robber     - steal[i] = max(steal[i-1], steal[i-2] + nums[i])

Complexity in simple words:
  A table with n cells costs O(n) time to fill (O(n * n) for a grid).
  The whole point of DP is that O(n^2) memoised recursion becomes
  O(n) once we remember the answers.

Tip: if you cannot explain the state in one short sentence, you do not
understand the problem yet. Write that sentence down first, then write
the code.
"""

from _dsa_kit import main


# ---------------------------------------------------------------------------
# DEMOS - run these first, then change the code and experiment
# ---------------------------------------------------------------------------


def demo_fib_memo() -> None:
    # Same recursion, but we remember every answer.
    calls = 0

    def slow_fib(n: int) -> int:
        nonlocal calls
        calls += 1
        if n < 2:
            return n
        return slow_fib(n - 1) + slow_fib(n - 2)

    memo = {0: 0, 1: 1}

    def fast_fib(n: int) -> int:
        if n in memo:
            return memo[n]
        memo[n] = fast_fib(n - 1) + fast_fib(n - 2)
        return memo[n]

    print("slow fib(20) =", slow_fib(20), "-> function calls:", calls)
    print("memo fib(20) =", fast_fib(20), "-> values cached:", len(memo))


def demo_climb_stairs() -> None:
    # You can climb 1 or 2 steps. ways[i] counts the ways to reach step i.
    n = 6
    ways = [1] * (n + 1)
    for step in range(2, n + 1):
        ways[step] = ways[step - 1] + ways[step - 2]
    print("steps:          ", list(range(n + 1)))
    print("ways to get there:", ways)
    print("step 5 = step 4 (1 step) + step 3 (2 steps).")


def demo_coin_change() -> None:
    # best[value] = fewest coins needed to make this amount.
    coins = [1, 2, 5]
    amount = 11
    best = [0] + [amount + 1] * amount
    for value in range(1, amount + 1):
        for coin in coins:
            if coin <= value and best[value - coin] + 1 < best[value]:
                best[value] = best[value - coin] + 1
    print("coins:", coins, "amount:", amount)
    print("fewest coins per amount:", best)
    print("answer for", amount, "=", best[amount], "-> 5 + 5 + 1")


def demo_lis() -> None:
    # best[i] = length of the longest increasing sequence ending at i.
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    best = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i] and best[j] + 1 > best[i]:
                best[i] = best[j] + 1
    print("nums:", nums)
    print("longest increasing part ending at each position:", best)
    print("LIS length:", max(best), "-> 2, 3, 7, 101")


def demo_grid_paths() -> None:
    # dp[r][c] = paths from the top-left corner to that cell.
    m, n = 4, 4
    dp = [[1] * n for _ in range(m)]
    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]
    print("paths to every cell (only right and down moves):")
    for row in dp:
        print("   ", row)
    print("corner to corner:", dp[m - 1][n - 1])


def demo_knapsack_and_robber() -> None:
    # Knapsack: each item can be taken once, so we go backwards.
    weights = [1, 2, 3]
    values = [6, 10, 12]
    capacity = 5
    best = [0] * (capacity + 1)
    for weight, value in zip(weights, values):
        for c in range(capacity, weight - 1, -1):
            if best[c - weight] + value > best[c]:
                best[c] = best[c - weight] + value
    print("items (weight, value):", list(zip(weights, values)), "capacity:", capacity)
    print("best value for each capacity:", best)
    print("greedy takes weight 3 first and gets", 12 + 6, "- the answer is", best[capacity])
    # House robber: you cannot rob two houses next to each other.
    houses = [2, 7, 9, 3, 1]
    prev2 = prev1 = 0
    for money in houses:
        prev2, prev1 = prev1, max(prev1, prev2 + money)
    print("houses:", houses, "-> best robbery:", prev1)


# ---------------------------------------------------------------------------
# EXERCISES - write your code where you see TODO
# ---------------------------------------------------------------------------


def climb_stairs(n: int) -> int:
    """Ways to reach step n when you can climb 1 or 2 steps at a time.
    climb_stairs(5) -> 8
    """
    # TODO: build a table of ways[0..n]
    return None

def min_coins(coins: list, amount: int) -> int:
    """Fewest coins that add up to amount, or -1 when it is not possible.
    min_coins([1, 2, 5], 11) -> 3
    """
    # TODO: for every amount try all coins and keep the best answer
    return None

def longest_increasing_subsequence(nums: list) -> int:
    """Length of the longest strictly increasing subsequence.
    longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18]) -> 4
    """
    # TODO: best[i] = longest increasing sequence that ends at i
    return None

def max_knapsack(weights: list, values: list, capacity: int) -> int:
    """Highest total value you can carry, using each item at most once.
    max_knapsack([1, 2, 3], [6, 10, 12], 5) -> 22
    """
    # TODO: a table of the best value for every capacity
    return None

def grid_paths(m: int, n: int) -> int:
    """Ways to go from the top-left to the bottom-right moving right/down.
    grid_paths(3, 3) -> 6
    """
    # TODO: fill a m x n table with the number of paths
    return None

def house_robber(nums: list) -> int:
    """Most money you can steal without robbing two neighbours.
    house_robber([2, 7, 9, 3, 1]) -> 12
    """
    # TODO: keep the best total up to the previous house
    return None

def count_paths_with_obstacles(grid: list) -> int:
    """Paths from top-left to bottom-right, where 1 means blocked.
    count_paths_with_obstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) -> 2
    """
    # TODO: build the path table, blocked cells always stay 0
    return None

def fib_memo(n: int) -> int:
    """The n-th fibonacci number, computed with a memo dict.
    fib_memo(10) -> 55
    """
    # TODO: remember every answer you already computed
    return None


# Solutions - try it yourself first, then run with `--solutions`
def sol_climb_stairs(n: int) -> int:
    if n <= 1:
        return 1
    ways = [0] * (n + 1)
    ways[0] = 1
    ways[1] = 1
    for step in range(2, n + 1):
        ways[step] = ways[step - 1] + ways[step - 2]
    return ways[n]

def sol_min_coins(coins: list, amount: int) -> int:
    best = [0] + [amount + 1] * amount
    for value in range(1, amount + 1):
        for coin in coins:
            if coin <= value and best[value - coin] + 1 < best[value]:
                best[value] = best[value - coin] + 1
    return best[amount] if best[amount] <= amount else -1

def sol_longest_increasing_subsequence(nums: list) -> int:
    if not nums:
        return 0
    best = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i] and best[j] + 1 > best[i]:
                best[i] = best[j] + 1
    return max(best)

def sol_max_knapsack(weights: list, values: list, capacity: int) -> int:
    best = [0] * (capacity + 1)
    for weight, value in zip(weights, values):
        # Go backwards so the same item is never used twice.
        for c in range(capacity, weight - 1, -1):
            if best[c - weight] + value > best[c]:
                best[c] = best[c - weight] + value
    return best[capacity]

def sol_grid_paths(m: int, n: int) -> int:
    if m <= 0 or n <= 0:
        return 0
    dp = [[1] * n for _ in range(m)]
    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]
    return dp[m - 1][n - 1]

def sol_house_robber(nums: list) -> int:
    prev2 = 0        # best total up to two houses back
    prev1 = 0        # best total up to the previous house
    for money in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + money)
    return prev1

def sol_count_paths_with_obstacles(grid: list) -> int:
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                dp[r][c] = 0                     # blocked, no way through
            elif r == 0 and c == 0:
                dp[r][c] = 1                     # one way to start
            else:
                above = dp[r - 1][c] if r > 0 else 0
                left = dp[r][c - 1] if c > 0 else 0
                dp[r][c] = above + left
    return dp[rows - 1][cols - 1]

def sol_fib_memo(n: int) -> int:
    if n <= 0:
        return 0
    memo = {0: 0, 1: 1}

    def fib(k: int) -> int:
        if k in memo:
            return memo[k]
        memo[k] = fib(k - 1) + fib(k - 2)
        return memo[k]
    return fib(n)


EXERCISES = [
    {
        "id": "15.1", "task": "climb_stairs(n): ways to climb n steps with 1 or 2 steps",
        "func": climb_stairs,
        "tests": [((5,), 8), ((3,), 3), ((1,), 1), ((10,), 89)],
        "solution": sol_climb_stairs,
    },
    {
        "id": "15.2", "task": "min_coins(coins, amount): fewest coins, or -1",
        "func": min_coins,
        "tests": [(([1, 2, 5], 11), 3), (([2, 5, 10], 27), 4), (([2], 3), -1), (([1], 0), 0)],
        "solution": sol_min_coins,
    },
    {
        "id": "15.3", "task": "longest_increasing_subsequence(nums): length of the LIS",
        "func": longest_increasing_subsequence,
        "tests": [(([10, 9, 2, 5, 3, 7, 101, 18],), 4), (([0, 1, 0, 3, 2, 3],), 4), (([7, 7, 7],), 1), (([],), 0)],
        "solution": sol_longest_increasing_subsequence,
    },
    {
        "id": "15.4", "task": "max_knapsack(weights, values, capacity): best total value",
        "func": max_knapsack,
        "tests": [(([1, 2, 3], [6, 10, 12], 5), 22), (([1, 3, 4], [15, 20, 30], 4), 35), (([5], [10], 4), 0)],
        "solution": sol_max_knapsack,
    },
    {
        "id": "15.5", "task": "grid_paths(m, n): paths from corner to corner",
        "func": grid_paths,
        "tests": [((3, 3), 6), ((2, 2), 2), ((1, 1), 1), ((3, 7), 28)],
        "solution": sol_grid_paths,
    },
    {
        "id": "15.6", "task": "house_robber(nums): most money without two neighbours",
        "func": house_robber,
        "tests": [(([1, 2, 3, 1],), 4), (([2, 7, 9, 3, 1],), 12), (([5],), 5), (([],), 0)],
        "solution": sol_house_robber,
    },
    {
        "id": "15.7", "task": "count_paths_with_obstacles(grid): paths with blocked cells",
        "func": count_paths_with_obstacles,
        "tests": [(([[0, 0, 0], [0, 1, 0], [0, 0, 0]],), 2), (([[0, 1], [0, 0]],), 1), (([[0, 0], [0, 0]],), 2), (([[1]],), 0)],
        "solution": sol_count_paths_with_obstacles,
    },
    {
        "id": "15.8", "task": "fib_memo(n): fibonacci with a memo dict",
        "func": fib_memo,
        "tests": [((10,), 55), ((0,), 0), ((1,), 1), ((30,), 832040)],
        "solution": sol_fib_memo,
    },
]

DEMOS = [
    ("1. Memoised fibonacci", demo_fib_memo),
    ("2. Climbing stairs", demo_climb_stairs),
    ("3. Coin change", demo_coin_change),
    ("4. Longest increasing subsequence", demo_lis),
    ("5. Grid paths", demo_grid_paths),
    ("6. Knapsack and house robber", demo_knapsack_and_robber),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
