"""
DSA 11 - Recursion and backtracking
===================================

Today's goal:
  1. See how a function can call itself
  2. Learn the 3 parts every recursive function needs
  3. Make slow recursion fast with memoisation
  4. Use backtracking to find ALL possible answers
  5. Know when recursion is too slow for Python

Recursion in one sentence:
  "To solve this problem, solve a smaller version of the same problem."

Every recursive function needs exactly 3 things:
  1. BASE CASE - the easy case where you already know the answer.
  2. RECURSIVE CASE - the call to yourself with a smaller problem.
  3. PROGRESS - the argument must get smaller every time, otherwise
     the calls never stop.

The shape of the code:
```python
def countdown(n):
    if n <= 0:          # 1. base case
        return
    countdown(n - 1)    # 2. recursive call, 3. n gets smaller
```

Why it works:
  Python keeps a stack of "waiting" calls. Every new call goes on top of
  the stack, and the answers travel back down it when the base case returns.

Memoisation - never solve the same problem twice:
  fib(5) is needed by fib(6) AND by fib(7). Without remembering, Python
  calculates fib(5) again and again: 22 000 calls for fib(20) naive, but
  only 21 calls with a memo - that is O(n), n steps and no log.

Backtracking - recursion plus UNDO:
  Some questions have many answers (all subsets, all permutations). Pick one
  choice, go deeper, then UNDO the choice before trying the next one - that
  undo step is the whole idea of backtracking.
  The number of answers can be 2^n - the power of two - so these problems
  are naturally slow. That is normal, not a bug.

Tip: write the base case FIRST, then the recursive case.
Tip: slow recursion? Look for repeated work - that is memoisation.
Tip: "RecursionError" means your base case is missing or wrong.
"""

from _dsa_kit import main


# ---------------------------------------------------------------------------
# DEMOS - run these first, then change the code and experiment
# ---------------------------------------------------------------------------


def demo_factorial() -> None:
    # 5! = 5 * 4 * 3 * 2 * 1 = 120. Each call asks for a smaller number.
    def factorial(n: int) -> int:
        if n <= 1:
            return 1                     # base case
        return n * factorial(n - 1)      # smaller problem

    for n in range(6):
        print(f"{n}! = {factorial(n)}")


def demo_fib_naive_vs_memo() -> None:
    # The slow version calculates the same numbers again and again.
    def fib_slow(n: int, counter: list) -> int:
        counter[0] += 1
        if n <= 1:
            return n
        return fib_slow(n - 1, counter) + fib_slow(n - 2, counter)
    # The fast version saves every answer in a dict - no number twice.
    def fib_fast(n: int, memo: dict) -> int:
        if n not in memo:
            memo[n] = fib_fast(n - 1, memo) + fib_fast(n - 2, memo)
        return memo[n]

    slow_count, fast_memo = [0], {0: 0, 1: 1}
    n = 20
    value = fib_slow(n, slow_count)
    fib_fast(n, fast_memo)
    print(f"fib({n}) = {value} in both versions")
    print(f"slow version made {slow_count[0]} calls, fast version only "
          f"visited {len(fast_memo)} different numbers")
    print("O(2^n) became O(n) - one step per number, no log needed.")


def demo_sum_digits() -> None:
    # % 10 gives the last digit, // 10 drops that last digit.
    def sum_digits(n: int) -> int:
        if n == 0:
            return 0
        return n % 10 + sum_digits(n // 10)

    for number in [1234, 99, 7]:
        print(f"{number} -> digits add up to {sum_digits(number)}")


def demo_power() -> None:
    # Slow: one multiplication for each power - O(b) steps.
    def power_slow(a: int, b: int) -> int:
        if b == 0:
            return 1
        return a * power_slow(a, b - 1)

    # Fast (see sol_power): square the base, halve the exponent.
    print("power_slow(2, 10) =", power_slow(2, 10), " power_fast(2, 10) =",
          sol_power(2, 10))
    print("power_fast(3, 5)  =", sol_power(3, 5))
    print("the log comes from halving the exponent every single step")


def demo_subsets() -> None:
    # Backtracking: take a number or skip it, then undo the choice.
    print("all subsets of [1, 2, 3]:")
    for group in sol_subsets([1, 2, 3]):
        print("   ", group)


def demo_permutations() -> None:
    # Same idea, but here the order matters, so every spot can be filled.
    print("all permutations of [1, 2, 3]:")
    for order in sol_permutations([1, 2, 3]):
        print("   ", order)


def demo_combination_sum() -> None:
    # Add numbers until the target is reached - a number may be used twice.
    print("ways to make 7 using [2, 3, 6, 7]:")
    for combo in sol_combination_sum([2, 3, 6, 7], 7):
        print("   ", combo)


def demo_grid_paths() -> None:
    # How many ways to walk to the bottom-right corner, right or down only?
    def count_paths(grid: list, r: int, c: int) -> int:
        if r < 0 or c < 0 or grid[r][c] == 1:
            return 0
        if r == 0 and c == 0:
            return 1
        return count_paths(grid, r - 1, c) + count_paths(grid, r, c - 1)

    grid = [[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 1, 0]]
    print("the grid (1 = wall):", grid)
    print("number of paths:", count_paths(grid, 3, 3))


# ---------------------------------------------------------------------------
# EXERCISES - write your code where you see TODO
# ---------------------------------------------------------------------------


def factorial(n: int) -> int:
    """Return n! - the product of 1, 2, ... up to n.
    factorial(5) -> 120
    """
    # TODO: base case n <= 1, then call yourself with n - 1
    return None


def fib(n: int) -> int:
    """Return the n-th Fibonacci number (0, 1, 1, 2, 3, 5, 8...) quickly.
    fib(10) -> 55
    """
    # TODO: save the answers in a dict so no number is calculated twice
    return None


def sum_digits(n: int) -> int:
    """Return the sum of the digits of a non-negative number.
    sum_digits(1234) -> 10
    """
    # TODO: take the last digit with % 10 and drop it with // 10
    return None


def power(a: int, b: int) -> int:
    """Return a to the power b (b >= 0), using the fast method.
    power(2, 10) -> 1024
    """
    # TODO: halve the exponent and square the result
    return None


def subsets(nums: list) -> list:
    """Return every subset of nums as a list of lists.
    subsets([1, 2]) -> [[], [1], [1, 2], [2]]
    """
    # TODO: take a number or skip it, then undo before the next one
    return None


def permutations(nums: list) -> list:
    """Return every ordering of nums as a list of lists.
    permutations([1, 2]) -> [[1, 2], [2, 1]]
    """
    # TODO: fill the answer from left to right and undo every choice
    return None


def combination_sum(nums: list, target: int) -> list:
    """Return all ways to reach target using numbers from nums.
    A number may be used more than once. combination_sum([2, 3], 4) -> [[2, 2]]
    """
    # TODO: pick a number, subtract it from the target, then undo
    return None


def tower_of_hanoi_moves(n: int) -> int:
    """Return how many moves the Tower of Hanoi needs for n discs.
    tower_of_hanoi_moves(3) -> 7
    """
    # TODO: the answer for n is twice the answer for n - 1, plus one
    return None


# Solutions - try it yourself first, then run with `--solutions`
def sol_factorial(n: int) -> int:
    if n <= 1:
        return 1
    return n * sol_factorial(n - 1)


def sol_fib(n: int) -> int:
    memo = {0: 0, 1: 1}

    def helper(k: int) -> int:
        if k not in memo:
            memo[k] = helper(k - 1) + helper(k - 2)
        return memo[k]

    return helper(n)


def sol_sum_digits(n: int) -> int:
    if n == 0:
        return 0
    return n % 10 + sol_sum_digits(n // 10)


def sol_power(a: int, b: int) -> int:
    if b == 0:
        return 1
    half = sol_power(a, b // 2)
    if b % 2 == 0:
        return half * half
    return a * half * half


def sol_subsets(nums: list) -> list:
    out: list = []

    def backtrack(start: int, path: list) -> None:
        out.append(path.copy())
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return out


def sol_permutations(nums: list) -> list:
    out: list = []

    def backtrack(path: list, left: list) -> None:
        if not left:
            out.append(path)
            return
        for i in range(len(left)):
            backtrack(path + [left[i]], left[:i] + left[i + 1:])

    backtrack([], nums)
    return out


def sol_combination_sum(nums: list, target: int) -> list:
    nums = sorted(nums)
    out: list = []

    def backtrack(start: int, left: int, path: list) -> None:
        if left == 0:
            out.append(path)
            return
        for i in range(start, len(nums)):
            if nums[i] > left:
                break
            backtrack(i, left - nums[i], path + [nums[i]])

    backtrack(0, target, [])
    return out


def sol_tower_of_hanoi_moves(n: int) -> int:
    if n <= 0:
        return 0
    return 2 * sol_tower_of_hanoi_moves(n - 1) + 1


EXERCISES = [
    {
        "id": "11.1", "task": "factorial(n): product of 1 up to n",
        "func": factorial, "tests": [((5,), 120), ((0,), 1)],
        "solution": sol_factorial,
    },
    {
        "id": "11.2", "task": "fib(n): n-th Fibonacci number, memoised",
        "func": fib, "tests": [((10,), 55), ((1,), 1)],
        "solution": sol_fib,
    },
    {
        "id": "11.3", "task": "sum_digits(n): add up all digits of n",
        "func": sum_digits, "tests": [((1234,), 10), ((999,), 27)],
        "solution": sol_sum_digits,
    },
    {
        "id": "11.4", "task": "power(a, b): a to the power b, computed fast",
        "func": power, "tests": [((2, 10), 1024), ((3, 5), 243)],
        "solution": sol_power,
    },
    {
        "id": "11.5", "task": "subsets(nums): every subset of the numbers",
        "func": subsets, "tests": [(([1, 2],), [[], [1], [1, 2], [2]]), (([],), [[]])],
        "solution": sol_subsets,
    },
    {
        "id": "11.6", "task": "permutations(nums): every ordering of the numbers",
        "func": permutations, "tests": [(([1, 2],), [[1, 2], [2, 1]]), (([1],), [[1]])],
        "solution": sol_permutations,
    },
    {
        "id": "11.7", "task": "combination_sum(nums, target): ways to reach target",
        "func": combination_sum, "tests": [(([2, 3, 6, 7], 7), [[2, 2, 3], [7]]), (([2], 6), [[2, 2, 2]])],
        "solution": sol_combination_sum,
    },
    {
        "id": "11.8", "task": "tower_of_hanoi_moves(n): moves needed for n discs",
        "func": tower_of_hanoi_moves, "tests": [((3,), 7), ((10,), 1023)],
        "solution": sol_tower_of_hanoi_moves,
    },
]

DEMOS = [
    ("1. Factorial", demo_factorial),
    ("2. Fibonacci: slow vs memoised", demo_fib_naive_vs_memo),
    ("3. Sum of digits", demo_sum_digits),
    ("4. Power: slow vs fast", demo_power),
    ("5. Generate subsets", demo_subsets),
    ("6. Generate permutations", demo_permutations),
    ("7. Combination sum", demo_combination_sum),
    ("8. Paths in a grid", demo_grid_paths),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
