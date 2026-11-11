"""
Chapter 00 - Absolute Beginner: Start Here
==========================================

Never written a line of code before? Perfect. This chapter assumes you know
nothing at all. We will go very slowly.

What is a program?
  - A program is a set of instructions for a computer.
  - The computer follows the instructions in order, like a recipe.
  - If you write "show Hello", the computer shows Hello on the screen.

What is Python?
  - Python is the language we use to write those instructions.
  - It is easy to read, almost like English.
  - A Python file ends with .py

What is a terminal?
  - The terminal is a text window where you type commands.
  - On Windows: press the Windows key, type PowerShell, then press Enter.
  - You type a command and press Enter to run it.

Check that Python is installed:
  python --version
  -> You should see something like: Python 3.12.10
  If you see an error, install Python from python.org and tick
  "Add Python to PATH" during installation.

Run a file:
  python chapters/00_absolute_basics.py

Try one line at a time (this is called the REPL):
  python
  >>> print("Hello")
  Hello
  >>> 2 + 3
  5
  >>> exit()

How to use this course:
  1. Read the notes.
  2. Run the demos and read the output.
  3. Solve the exercises. They are small on purpose.
  4. Mark the chapter complete in the portal.

Three habits that matter:
  - Type the code yourself. Do not only copy-paste.
  - Run the code often. Change one thing and run it again.
  - Errors are normal. Read the last line of the error message.

Ready? Let's write your first line.
"""

from _kit import main


# ---------------------------------------------------------------------------
# DEMOS - run these first, then change the code and experiment
# ---------------------------------------------------------------------------


def demo_first_line() -> None:
    # print() shows text on the screen.
    print("Hello, world!")
    print("This is my first Python line.")
    print("I can print numbers too:", 7)


def demo_math() -> None:
    # Python can do math.
    print("2 + 3 =", 2 + 3)
    print("10 - 4 =", 10 - 4)
    print("3 * 4 =", 3 * 4)
    print("10 / 2 =", 10 / 2)


def demo_variables() -> None:
    # A variable is a name that stores a value.
    name = "Ravi"
    age = 21
    print("Name:", name)
    print("Age:", age)
    print("Next year age:", age + 1)


def demo_comments() -> None:
    # A comment starts with #. Python ignores it.
    # Comments explain your code to humans.
    print("Comments do not change the output.")


# ---------------------------------------------------------------------------
# EXERCISES - write your code where you see TODO
# ---------------------------------------------------------------------------


def say_hello() -> str:
    """Return the text "Hello!".

    say_hello() -> "Hello!"
    """
    # TODO: return the text "Hello!"
    return None


def answer() -> int:
    """Return the number 42.

    answer() -> 42
    """
    # TODO: return the number 42
    return None


def add_one(number: int) -> int:
    """Return number + 1.

    add_one(5) -> 6
    """
    # TODO: return number + 1
    return None


def introduce(name: str) -> str:
    """Return "My name is <name>".

    introduce("Ravi") -> "My name is Ravi"
    """
    # TODO: join the text and the name
    return None


# Solutions - try it yourself first, then run with `--solutions`
def sol_say_hello() -> str:
    return "Hello!"


def sol_answer() -> int:
    return 42


def sol_add_one(number: int) -> int:
    return number + 1


def sol_introduce(name: str) -> str:
    return "My name is " + name


EXERCISES = [
    {
        "id": "0.1",
        "task": "say_hello(): return the text 'Hello!'",
        "func": say_hello,
        "tests": [((), "Hello!")],
        "solution": sol_say_hello,
    },
    {
        "id": "0.2",
        "task": "answer(): return the number 42",
        "func": answer,
        "tests": [((), 42)],
        "solution": sol_answer,
    },
    {
        "id": "0.3",
        "task": "add_one(number): return number + 1",
        "func": add_one,
        "tests": [((5,), 6), ((0,), 1)],
        "solution": sol_add_one,
    },
    {
        "id": "0.4",
        "task": "introduce(name): return 'My name is <name>'",
        "func": introduce,
        "tests": [(("Ravi",), "My name is Ravi")],
        "solution": sol_introduce,
    },
]

DEMOS = [
    ("1. Your first print()", demo_first_line),
    ("2. Python does math", demo_math),
    ("3. Variables", demo_variables),
    ("4. Comments", demo_comments),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
