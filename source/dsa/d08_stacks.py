"""
DSA 08 - Stacks (last in, first out)
====================================

Today's goal:
  1. Understand what a stack is and why "last in, first out" matters
  2. Use a plain Python list as a stack: push, pop, peek
  3. Solve the classic stack problems: brackets, next greater, postfix
  4. Build a min stack that can return the smallest value in O(1)

What is a stack?
  A stack is a pile of plates. You put a plate on top (push) and you
  take the top plate off (pop). The plate you put in last is the plate
  you take out first. That is why we call it LIFO:
    LIFO = Last In, First Out

In Python a list IS already a stack:
```python
stack = []
stack.append(5)      # push  (add to the end)
stack.append(3)      # push
stack[-1]            # peek  (look at the top, do not remove it)
stack.pop()          # pop   (remove the top)
```
append and pop are O(1) - they are instant, nothing has to move.

Three operations you must remember: push(x) puts x on top, pop() takes
the top off and peek() only looks at the top without taking it off.

Why stacks are useful:
  - Brackets must close in the reverse order they opened -> stack
  - Undo and redo in an editor, and the function call stack -> stack
  - Next greater element -> a monotonic stack

The pattern for "matching pairs":
  Push every opening symbol. When a closing symbol shows up, the top of
  the stack MUST be its partner - if it is not, the text is broken.

The pattern for "next greater element":
  Go from left to right. The stack holds indexes whose value is still
  waiting for a bigger number. When the current value beats the value
  on top, that top index has found its answer - pop it and write the
  current value down. This is O(n): every index is pushed and popped
  only once.

Time complexity in plain words:
  push / pop / peek   -> O(1), instant
  one full traversal  -> O(n), one pass through the data

Tip: when you write "stack", picture a vertical pile where only the top
is visible. If your code needs the second item from the front, you are
probably using the wrong structure - try a queue instead (chapter 9).
"""

from _dsa_kit import main


# ---------------------------------------------------------------------------
# DEMOS - run these first, then change the code and experiment
# ---------------------------------------------------------------------------


def demo_stack_from_list() -> None:
    # A stack is just a list. The end of the list is the top of the stack.
    stack = []
    stack.append(10)      # push
    stack.append(20)      # push
    stack.append(30)      # push
    print("stack after 3 pushes :", stack)
    print("peek (top, no remove):", stack[-1])
    for _ in range(3):
        print("pop                  :", stack.pop(), "-> stack is now", stack)


def demo_valid_parentheses() -> None:
    # Every closing bracket must match the top of the stack.
    text = "(a + b) [c{d}]"
    stack = []
    pairs = {")": "(", "]": "[", "}": "{"}
    for ch in text:
        if ch in "([{":
            stack.append(ch)
            print(f"push  {ch!r:4} stack -> {stack}")
        elif ch in pairs:
            top = stack.pop() if stack else None
            print(f"close {ch!r:4} top was {top!r:4} match: {top == pairs[ch]}")
    print("left on the stack:", stack, "(empty means everything matched)")


def demo_next_greater() -> None:
    # A monotonic stack: the indexes wait for a bigger number.
    arr = [2, 1, 3, 4, 3]
    result = [-1] * len(arr)
    stack = []          # indexes that are still waiting
    for i, value in enumerate(arr):
        while stack and arr[stack[-1]] < value:
            index = stack.pop()
            result[index] = value
            print(f"{value} is bigger than arr[{index}] = {arr[index]}")
        stack.append(i)
    print("next greater element:", result)


def demo_min_stack() -> None:
    # A second stack keeps the smallest value seen so far.
    stack = []
    mins = []
    for value in [5, 3, 7, 2]:
        stack.append(value)
        mins.append(min(value, mins[-1]) if mins else value)
        print(f"push {value} -> stack {stack}, smallest so far {mins[-1]}")
    stack.pop()
    mins.pop()
    print("after one pop the smallest is still", mins[-1])


def demo_postfix() -> None:
    # In postfix notation the operator comes after its numbers.
    expr = "3 4 2 * +"
    stack = []
    for token in expr.split():
        if token.isdigit():
            stack.append(int(token))
            print(f"push number {token} -> stack {stack}")
        else:
            right = stack.pop()
            left = stack.pop()
            if token == "+":
                value = left + right
            else:
                value = left * right
            stack.append(value)
            print(f"apply {left} {token} {right} = {value} -> stack {stack}")
    print("the value of the expression is", stack[-1])


def demo_reverse_with_stack() -> None:
    # A stack reverses the order for free.
    text = "stack"
    stack = []
    for ch in text:
        stack.append(ch)
    print("pushed   :", stack)
    out = ""
    while stack:
        out += stack.pop()
    print(f"{text!r} reversed with a stack -> {out!r} (push and pop are O(1))")


# ---------------------------------------------------------------------------
# EXERCISES - write your code where you see TODO
# ---------------------------------------------------------------------------


def is_valid_parentheses(s: str) -> bool:
    """Return True if every bracket in s has a matching pair in the right order.

    is_valid_parentheses("()[]{}") -> True
    """
    # TODO: push the opening brackets and match them on the way out
    return None


def next_greater_element(arr: list) -> list:
    """Return for each number the first bigger number to its right (-1 if none).

    next_greater_element([2, 1, 3]) -> [3, 3, -1]
    """
    # TODO: keep a stack of indexes that are waiting for a bigger number
    return None


def evaluate_postfix(expr: str) -> int:
    """Evaluate a postfix expression made of single digits and + - * /.

    Division is whole-number division, so 9 3 / gives 3.
    evaluate_postfix("3 4 +") -> 7
    """
    # TODO: push the numbers and apply the operators to the top two values
    return None


def min_stack_ops(operations: list) -> list:
    """Run the stack commands and collect the answer of every "min" and "top".

    The commands are: "push X", "pop", "min" and "top".
    min_stack_ops(["push 3", "push 1", "min"]) -> [1]
    """
    # TODO: keep a stack of values and a stack of the smallest value so far
    return None


def longest_valid_parentheses(s: str) -> int:
    """Return the length of the longest valid () part inside s.

    longest_valid_parentheses("(()") -> 2
    """
    # TODO: use a stack of indexes to mark the ends of valid parts
    return None


def remove_outer_parentheses(s: str) -> str:
    """Remove the outermost pair of brackets from every group in s.

    remove_outer_parentheses("(()())(())") -> "()()()"
    """
    # TODO: count how deep we are and keep only the inner brackets
    return None


# Solutions - try it yourself first, then run with `--solutions`
def sol_is_valid_parentheses(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack


def sol_next_greater_element(arr: list) -> list:
    result = [-1] * len(arr)
    stack = []          # indexes that are still waiting for a bigger number
    for i, value in enumerate(arr):
        while stack and arr[stack[-1]] < value:
            result[stack.pop()] = value
        stack.append(i)
    return result


def sol_evaluate_postfix(expr: str) -> int:
    stack = []
    for token in expr.split():
        if token in "+-*/":
            right = stack.pop()
            left = stack.pop()
            if token == "+":
                stack.append(left + right)
            elif token == "-":
                stack.append(left - right)
            elif token == "*":
                stack.append(left * right)
            else:
                stack.append(left // right)
        else:
            stack.append(int(token))
    return stack[-1] if stack else 0


def sol_min_stack_ops(operations: list) -> list:
    values = []
    mins = []
    answers = []
    for op in operations:
        parts = op.split()
        if parts[0] == "push":
            value = int(parts[1])
            values.append(value)
            mins.append(min(value, mins[-1]) if mins else value)
        elif parts[0] == "pop":
            if values:
                values.pop()
                mins.pop()
        elif parts[0] == "min":
            answers.append(mins[-1] if mins else None)
        elif parts[0] == "top":
            answers.append(values[-1] if values else None)
    return answers


def sol_longest_valid_parentheses(s: str) -> int:
    stack = [-1]         # -1 is the "floor" before the string starts
    best = 0
    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)          # this ")" is the new floor
            else:
                best = max(best, i - stack[-1])
    return best


def sol_remove_outer_parentheses(s: str) -> str:
    result = []
    depth = 0
    for ch in s:
        if ch == "(":
            if depth > 0:
                result.append(ch)
            depth += 1
        else:
            depth -= 1
            if depth > 0:
                result.append(ch)
    return "".join(result)


EXERCISES = [
    {
        "id": "8.1",
        "task": "is_valid_parentheses(s): True if the brackets match up",
        "func": is_valid_parentheses,
        "tests": [(("()[]{}",), True), (("([{}])",), True), (("(]",), False), (("",), True)],
        "solution": sol_is_valid_parentheses,
    },
    {
        "id": "8.2",
        "task": "next_greater_element(arr): the first bigger number to the right",
        "func": next_greater_element,
        "tests": [(([2, 1, 3, 4, 3],), [3, 3, 4, -1, -1]), (([5, 4, 3, 2, 1],), [-1, -1, -1, -1, -1])],
        "solution": sol_next_greater_element,
    },
    {
        "id": "8.3",
        "task": "evaluate_postfix(expr): work out the value of a postfix expression",
        "func": evaluate_postfix,
        "tests": [(("3 4 +",), 7), (("5 2 *",), 10), (("10 3 - 2 *",), 14), (("9 3 /",), 3)],
        "solution": sol_evaluate_postfix,
    },
    {
        "id": "8.4",
        "task": 'min_stack_ops(operations): answer every "min" and "top" command',
        "func": min_stack_ops,
        "tests": [((["push 3", "push 1", "min", "pop", "min", "top"],), [1, 3, 3]), ((["push 5", "min"],), [5])],
        "solution": sol_min_stack_ops,
    },
    {
        "id": "8.5",
        "task": "longest_valid_parentheses(s): length of the longest valid () part",
        "func": longest_valid_parentheses,
        "tests": [(("(()",), 2), ((")()())",), 4), (("()(())",), 6), (("",), 0)],
        "solution": sol_longest_valid_parentheses,
    },
    {
        "id": "8.6",
        "task": "remove_outer_parentheses(s): drop the outer pair of every group",
        "func": remove_outer_parentheses,
        "tests": [(("(()())(())",), "()()()"), (("(()())",), "()()"), (("",), "")],
        "solution": sol_remove_outer_parentheses,
    },
]

DEMOS = [
    ("1. A stack from a list", demo_stack_from_list),
    ("2. Valid parentheses", demo_valid_parentheses),
    ("3. Next greater element", demo_next_greater),
    ("4. A min stack", demo_min_stack),
    ("5. Postfix evaluation", demo_postfix),
    ("6. Reverse with a stack", demo_reverse_with_stack),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
