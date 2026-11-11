"""
Chapter 06 - Loops (Doing things again and again)
=================================================

Today's goal:
  1. for loop + range()
  2. while loop
  3. break, continue, and the loop's else
  4. Nested loops and patterns
  5. The accumulator pattern (finding a total, a count, a max)

for loop:
  for i in range(5):        # 0,1,2,3,4
      print(i)

  for ch in "abc":          # characters of a string
      print(ch)

  for item in [10, 20]:     # items of a list
      print(item)

The 3 forms of range:
  range(5)        -> 0 1 2 3 4
  range(2, 6)     -> 2 3 4 5
  range(1, 10, 2) -> 1 3 5 7 9
  range(5, 0, -1) -> 5 4 3 2 1

while loop: as long as the condition stays True.
  break    -> leave the loop
  continue -> jump to the next iteration
"""

from _kit import main


# ---------------------------------------------------------------------------
# DEMOS
# ---------------------------------------------------------------------------


def demo_for_range() -> None:
    print("range(5):", end=" ")
    for i in range(5):
        print(i, end=" ")
    print()

    print("range(2, 6):", end=" ")
    for i in range(2, 6):
        print(i, end=" ")
    print()

    print("range(1, 10, 2):", end=" ")
    for i in range(1, 10, 2):
        print(i, end=" ")
    print()

    print("range(5, 0, -1):", end=" ")
    for i in range(5, 0, -1):
        print(i, end=" ")
    print()

    for ch in "Python":
        print(ch, end="-")
    print()

    # A list straight from range
    print(list(range(1, 6)))
    print(sum(range(1, 101)))   # sum from 1 to 100


def demo_while() -> None:
    n = 5
    while n > 0:
        print("n =", n)
        n -= 1          # forget this line and you get an infinite loop!
    print("Liftoff!")

    # Digit sum with a while loop
    number = 9875
    total = 0
    while number > 0:
        total += number % 10
        number //= 10
    print("Sum of the digits of 9875:", total)


def demo_break_continue() -> None:
    # break: stop as soon as you find the first even number
    for n in [1, 3, 4, 7, 8]:
        if n % 2 == 0:
            print("first even:", n)
            break

    # continue: skip the odd numbers
    print("evens:", end=" ")
    for n in range(1, 11):
        if n % 2 != 0:
            continue
        print(n, end=" ")
    print()

    # while + break (menu style)
    attempts = 0
    while True:
        attempts += 1
        if attempts == 3:
            print("break after 3 attempts")
            break


def demo_loop_else() -> None:
    # else runs when the loop finishes without hitting break
    n = 7
    for i in range(2, n):
        if n % i == 0:
            print(n, "is not prime")
            break
    else:
        print(n, "is prime")

    n = 9
    for i in range(2, n):
        if n % i == 0:
            print(n, "is not prime")
            break
    else:
        print(n, "is prime")


def demo_nested_and_pattern() -> None:
    # Table
    for i in range(1, 4):
        for j in range(1, 4):
            print(i * j, end="\t")
        print()

    # Star triangle
    rows = 4
    for i in range(1, rows + 1):
        print("*" * i)

    # Upside-down triangle
    for i in range(rows, 0, -1):
        print(" " * (rows - i) + "*" * i)

    # Number pyramid
    for i in range(1, 5):
        print(str(i) * i)


def demo_accumulators() -> None:
    numbers = [4, 7, 2, 9, 1]

    total = 0
    for n in numbers:
        total += n
    print("sum:", total, "| average:", total / len(numbers))

    largest = numbers[0]
    for n in numbers:
        if n > largest:
            largest = n
    print("largest:", largest)

    count_even = 0
    for n in numbers:
        if n % 2 == 0:
            count_even += 1
    print("even count:", count_even)


# ---------------------------------------------------------------------------
# EXERCISES
# ---------------------------------------------------------------------------


def sum_to(n: int) -> int:
    """The sum from 1 to n (using a loop). sum_to(5) -> 15"""
    # TODO
    return None


def factorial(n: int) -> int:
    """n! = 1*2*...*n. factorial(0) -> 1, factorial(5) -> 120"""
    # TODO
    return None


def count_digits(n: int) -> int:
    """Count the digits. count_digits(0) -> 1, count_digits(1234) -> 4
    Use abs() for negative numbers.
    """
    # TODO
    return None


def reverse_number(n: int) -> int:
    """Reverse the digits of a number. reverse_number(1234) -> 4321
    reverse_number(1200) -> 21
    """
    # TODO: while loop + % 10 + // 10
    return None


def is_prime(n: int) -> bool:
    """Prime check. 0 and 1 are not prime. 2 is prime."""
    # TODO
    return None


def star_pattern(rows: int) -> str:
    """Return the triangle pattern as a string, with lines joined by \\n.
    star_pattern(3) -> "*\\n**\\n***"
    """
    # TODO: list + join or a loop
    return None


# Solutions
def sol_sum_to(n: int) -> int:
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


def sol_factorial(n: int) -> int:
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def sol_count_digits(n: int) -> int:
    n = abs(n)
    if n == 0:
        return 1
    count = 0
    while n > 0:
        count += 1
        n //= 10
    return count


def sol_reverse_number(n: int) -> int:
    rev = 0
    while n > 0:
        rev = rev * 10 + n % 10
        n //= 10
    return rev


def sol_is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def sol_star_pattern(rows: int) -> str:
    return "\n".join("*" * i for i in range(1, rows + 1))


EXERCISES = [
    {"id": "6.1", "task": "sum_to(n): the sum of 1..n", "func": sum_to,
     "tests": [((5,), 15), ((1,), 1), ((100,), 5050)], "solution": sol_sum_to},
    {"id": "6.2", "task": "factorial(n): the factorial of n", "func": factorial,
     "tests": [((0,), 1), ((5,), 120), ((3,), 6)], "solution": sol_factorial},
    {"id": "6.3", "task": "count_digits(n): how many digits", "func": count_digits,
     "tests": [((0,), 1), ((1234,), 4), ((-99,), 2)], "solution": sol_count_digits},
    {"id": "6.4", "task": "reverse_number(n): reverse the digits", "func": reverse_number,
     "tests": [((1234,), 4321), ((1200,), 21), ((7,), 7)], "solution": sol_reverse_number},
    {"id": "6.5", "task": "is_prime(n): prime check", "func": is_prime,
     "tests": [((2,), True), ((17,), True), ((18,), False), ((1,), False), ((0,), False)],
     "solution": sol_is_prime},
    {"id": "6.6", "task": "star_pattern(rows): '*\\n**\\n***'", "func": star_pattern,
     "tests": [((3,), "*\n**\n***"), ((1,), "*")], "solution": sol_star_pattern},
]

DEMOS = [
    ("6. for and range", demo_for_range),
    ("7. while", demo_while),
    ("8. break and continue", demo_break_continue),
    ("9. the loop's else", demo_loop_else),
    ("10. Nested loops and patterns", demo_nested_and_pattern),
    ("11. Accumulator patterns", demo_accumulators),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
