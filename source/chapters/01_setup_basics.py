"""
Chapter 01 - Setup and your first program
=========================================

Today's goal:
  1. Run a Python file from the terminal
  2. Show output with print()
  3. Understand comments and indentation
  4. The idea of input() (talking to the user)

What is Python?
  - A simple, readable programming language. Don't be scared by the name.
  - Files use the .py extension.
  - Code runs line by line (top to bottom).

How to run it:
  python chapters/01_setup_basics.py        <- run the file
  python                                    <- REPL (try mode), type exit() to close

Important things to know:
  - Indentation (the empty space at the start of a line) MATTERS in Python. Use 4 spaces.
  - Comment: Python ignores everything after #. Use it for notes.
  - print("...") writes to the screen.
  - input("...") takes one line from the user and ALWAYS gives you a string.
  - If you get an error, don't panic: read the last line, it tells you the real problem.
"""

from _kit import main, section


# ---------------------------------------------------------------------------
# DEMOS - run these first, then change the code and experiment
# ---------------------------------------------------------------------------


def demo_print() -> None:
    print("Hello, world!")
    print("My name is Ravi.")
    print("Python", "is", "easy", "to", "learn")          # comma joins with a space
    print("Python", "is", "easy", "to", "learn", sep="-")  # sep = what goes in between
    print("This line won't end yet...", end=" ")
    print("...now it has ended.")

    # Numbers and expressions can be printed too
    print(2 + 3)
    print("2 + 3 =", 2 + 3)

    # Multi-line print
    print("""
    One
      two
        three
    """)


def demo_comments_and_indent() -> None:
    # This is a comment. Python doesn't read it.
    x = 10  # you can also write a comment after a line

    if x > 5:
        # this block is inside because it is 4 spaces in
        print("x is greater than 5")
        print("this is also inside the if")
    print("this is outside the if")

    # Wrong indentation causes an error. Uncomment the line below and try it:
    #   print("I am wrong")
    # Error: IndentationError: unexpected indent


def demo_input_concept() -> None:
    # We are not auto-running input() here, otherwise the file would wait for you.
    # Run the code below in your REPL or in a new file:
    #
    #   name = input("Your name: ")
    #   print("Hello,", name)
    #
    # input() always gives you a STRING:
    #   age = input("Age: ")       # you get "21", not 21
    #   age = int(age)             # now it is a number
    #
    # Run the file and try it yourself:
    print("The input() example is in the comments. Create a new file and try it.")


def demo_errors() -> None:
    # Reading errors is the most important skill to learn. Let's make one on purpose.
    try:
        result = 10 / 0
        print(result)
    except ZeroDivisionError as e:
        print("Error caught:", e)
        print("Meaning: you cannot divide a number by 0.")

    # Common errors:
    #   NameError        -> wrong variable name / variable not defined
    #   TypeError        -> wrong type (for example "5" + 5)
    #   ValueError       -> right type but wrong value (int("hello"))
    #   IndentationError -> wrong spaces
    #   SyntaxError      -> the structure of the code itself is wrong
    try:
        print("5" + 5)
    except TypeError as e:
        print("TypeError:", e)
    try:
        int("hello")
    except ValueError as e:
        print("ValueError:", e)


# ---------------------------------------------------------------------------
# EXERCISES - write your code where you see TODO
# ---------------------------------------------------------------------------


def greet(name: str) -> str:
    """Return a greeting message.

    greet("Ravi") -> "Hello, Ravi!"
    """
    # TODO: write your code here
    return None


def add(a: int, b: int) -> int:
    """Return the sum of two numbers.

    add(2, 3) -> 5
    """
    # TODO
    return None


def rectangle_area(length: float, width: float) -> float:
    """Area of a rectangle = length * width.

    rectangle_area(4, 5) -> 20
    """
    # TODO
    return None


def minutes_to_hms(total_minutes: int) -> str:
    """Turn minutes into the format "Xh Ym".

    minutes_to_hms(125) -> "2h 5m"
    minutes_to_hms(60)  -> "1h 0m"
    """
    # TODO: hours = total_minutes // 60, mins = total_minutes % 60
    return None


# Solutions - try it yourself first, then look with `--solutions`
def sol_greet(name: str) -> str:
    return f"Hello, {name}!"


def sol_add(a: int, b: int) -> int:
    return a + b


def sol_rectangle_area(length: float, width: float) -> float:
    return length * width


def sol_minutes_to_hms(total_minutes: int) -> str:
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours}h {minutes}m"


EXERCISES = [
    {
        "id": "1.1",
        "task": "greet(name): use an f-string to return 'Hello, <name>!'",
        "func": greet,
        "tests": [(("Ravi",), "Hello, Ravi!"), (("Sita",), "Hello, Sita!")],
        "solution": sol_greet,
    },
    {
        "id": "1.2",
        "task": "add(a, b): return the sum of both numbers",
        "func": add,
        "tests": [((2, 3), 5), ((-1, 1), 0), ((10, 0), 10)],
        "solution": sol_add,
    },
    {
        "id": "1.3",
        "task": "rectangle_area(length, width): return the area",
        "func": rectangle_area,
        "tests": [((4, 5), 20), ((2.5, 4), 10.0)],
        "solution": sol_rectangle_area,
    },
    {
        "id": "1.4",
        "task": "minutes_to_hms(total): return a string like '2h 5m'",
        "func": minutes_to_hms,
        "tests": [((125,), "2h 5m"), ((60,), "1h 0m"), ((5,), "0h 5m")],
        "solution": sol_minutes_to_hms,
    },
]

DEMOS = [
    ("1. print() basics", demo_print),
    ("2. Comments and indentation", demo_comments_and_indent),
    ("3. The idea of input()", demo_input_concept),
    ("4. How to read errors", demo_errors),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
