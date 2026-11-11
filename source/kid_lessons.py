"""
kid_lessons.py - A super simple version of every chapter, written for a
10 year old kid.

Each lesson has:
  title  - a fun name for the topic
  story  - 2-3 short sentences with an easy example (a robot, a school bag...)
  points - 4-5 very simple facts, one line each
  code   - a tiny runnable program (5 lines or less)
  win    - what you can do after reading it

The portal uses this for "Kid Mode". The normal notes stay in the chapters.
"""

LESSONS = {
    "00": {
        "title": "Your computer is a very obedient robot",
        "story": (
            "A computer never guesses anything. It only does exactly what you tell it, "
            "line by line, from top to bottom. Tell it to say Hello, it says Hello. "
            "Forget to tell it something, it stays quiet."
        ),
        "points": [
            "Everything you write is an instruction for the robot.",
            "print(\"...\") makes words appear on the screen.",
            "Text needs quotes around it. Numbers do not.",
            "The robot reads your program from the top line to the bottom line.",
            "An error is not a disaster. It just means the robot did not understand.",
        ],
        "code": (
            "print(\"Hello! I am your computer.\")\n"
            "print(2 + 3)\n"
            "print(\"My name is Ravi and I am 21\")"
        ),
        "win": "You can now make your computer say anything you want.",
    },
    "01": {
        "title": "Waking up the robot (setup)",
        "story": (
            "Before you can talk to your robot you need the box where you type to it. "
            "That box is called the terminal. On Windows it is called PowerShell. "
            "Type python inside it and the robot wakes up and listens."
        ),
        "points": [
            "Open PowerShell: press the Windows key, type PowerShell, press Enter.",
            "Type python --version to check the robot is installed.",
            "Type python my_program.py to run a whole program.",
            "Type python alone to try one line at a time (the REPL).",
            "A # starts a note for humans. The robot ignores everything after #.",
        ],
        "code": (
            "# this is a note for humans only\n"
            "print(\"My very first program!\")\n"
            "print(\"I am ready to learn Python.\")"
        ),
        "win": "You can now run a Python file from the terminal.",
    },
    "02": {
        "title": "Boxes with names (variables)",
        "story": (
            "A variable is a box with a label on it. You put something inside and write "
            "the label on it. Later you just say the label instead of repeating the "
            "whole thing."
        ),
        "points": [
            "name = \"Ravi\" puts the text Ravi inside the box called name.",
            "age = 21 puts the number 21 inside the box called age.",
            "int(\"21\") turns text into a number, str(21) turns a number into text.",
            "f\"Hi {name}\" drops a value inside a sentence.",
            "Python knows the type: int, float, str, bool.",
        ],
        "code": (
            "name = \"Ravi\"\n"
            "age = 21\n"
            "print(f\"{name} is {age} years old\")\n"
            "print(\"Next year:\", age + 1)"
        ),
        "win": "You can now keep things safe in named boxes and print them nicely.",
    },
    "03": {
        "title": "The maths signs (operators)",
        "story": (
            "Operators are the symbols your robot uses to calculate, compare and check. "
            "Same as the maths symbols you already know, plus a few new ones."
        ),
        "points": [
            "+ - * / do normal maths.",
            "// divides and throws away the decimal. % gives the leftover.",
            "== means \"is equal to\" and != means \"not equal to\".",
            "> < >= <= compare two things.",
            "and, or, not join checks together.",
        ],
        "code": (
            "print(10 + 3)\n"
            "print(10 // 3)   # 3, the decimal is dropped\n"
            "print(10 % 3)    # 1, the leftover\n"
            "print(10 > 3)    # True"
        ),
        "win": "You can now calculate and compare anything.",
    },
    "04": {
        "title": "Words as ribbons (strings)",
        "story": (
            "Text in Python is called a string. Think of it as a long ribbon of letters. "
            "You can cut the ribbon into pieces, clean it, and glue pieces back together."
        ),
        "points": [
            "\"hello\" is a string. Quotes are the handles of the ribbon.",
            "s[0] gets the first letter. s[0:3] gets the first three letters.",
            ".upper() and .lower() change the case. .strip() removes extra spaces.",
            ".split() cuts text into a list. \"-\".join(list) glues it back.",
            "f-strings let you mix values and text in one sentence.",
        ],
        "code": (
            "name = \"  RAVI  \"\n"
            "print(name.strip().lower())\n"
            "words = \"I am learning Python\".split()\n"
            "print(len(words))"
        ),
        "win": "You can now cut, clean and glue text.",
    },
    "05": {
        "title": "Making choices (if / else)",
        "story": (
            "Your robot can choose. if means \"if this is true, do this\". "
            "else means \"otherwise do that\". Like a traffic light: green means go, "
            "red means stop."
        ),
        "points": [
            "if, elif and else decide which code runs.",
            "The condition uses ==, >, < and friends.",
            "Indentation (4 spaces) shows what belongs to the if.",
            "else runs when nothing else matched.",
            "You can write a one-line if with a ternary.",
        ],
        "code": (
            "age = 21\n"
            "if age >= 18:\n"
            "    print(\"You can vote.\")\n"
            "else:\n"
            "    print(\"Too young.\")"
        ),
        "win": "You can now make your robot decide things by itself.",
    },
    "06": {
        "title": "Doing it again (loops)",
        "story": (
            "Loops stop you from typing the same thing again and again. "
            "Like brushing your teeth: you repeat the same steps until the job is done."
        ),
        "points": [
            "for i in range(5): repeats 5 times.",
            "while repeats until the condition becomes False.",
            "break stops the loop early. continue jumps to the next round.",
            "The loop variable changes every round (1, 2, 3...).",
            "range(start, stop, step) controls the counting.",
        ],
        "code": (
            "for i in range(1, 4):\n"
            "    print(\"Round\", i)\n"
            "\n"
            "count = 0\n"
            "while count < 3:\n"
            "    print(\"still counting\", count)\n"
            "    count += 1"
        ),
        "win": "You can now repeat any boring task automatically.",
    },
    "07": {
        "title": "A shelf of things (lists)",
        "story": (
            "A list is a shelf where you keep many things in order, like the books in "
            "your school bag. You can add, remove, find and sort them."
        ),
        "points": [
            "items = [\"pen\", \"book\"] creates a list.",
            "items[0] is the first one, items[-1] is the last one.",
            ".append(x) adds at the end, .insert(i, x) adds in the middle.",
            ".remove(x) deletes it, .pop() takes the last one out.",
            "sorted() sorts, .reverse() turns it around.",
        ],
        "code": (
            "fruits = [\"apple\", \"banana\"]\n"
            "fruits.append(\"mango\")\n"
            "print(fruits[0])\n"
            "print(len(fruits))"
        ),
        "win": "You can now manage a whole group of things.",
    },
    "08": {
        "title": "Locked boxes and magic bags (tuples & sets)",
        "story": (
            "A tuple is a locked box. You can look inside but you cannot change it. "
            "A set is a magic bag: it only keeps one copy of each thing."
        ),
        "points": [
            "(1, 2) is a tuple. Its values can never change.",
            "{1, 2, 3} is a set. No duplicates allowed.",
            "| is union (both together), & is common, - is difference.",
            "Sets are very fast at finding duplicates.",
            "A set has no order, so items come out in a random order.",
        ],
        "code": (
            "a = {1, 2, 3}\n"
            "b = {3, 4}\n"
            "print(a & b)   # {3} - the common ones\n"
            "print(a | b)   # all of them"
        ),
        "win": "You can now keep safe fixed groups and remove duplicates.",
    },
    "09": {
        "title": "Label to value (dictionaries)",
        "story": (
            "A dictionary is like a school roll. The roll number is the key, and it "
            "points to the name. You can find any name in one second."
        ),
        "points": [
            "marks = {\"Ravi\": 90} creates a dictionary.",
            "d[\"Ravi\"] gets the value. d.get(\"Ravi\", 0) is the safe version.",
            "\"Ravi\" in d checks if the key exists.",
            ".keys(), .values(), .items() give you the parts.",
            "Counting is easy: d[word] = d.get(word, 0) + 1.",
        ],
        "code": (
            "marks = {\"Ravi\": 90, \"Sita\": 80}\n"
            "for name, score in marks.items():\n"
            "    print(name, \"scored\", score)"
        ),
        "win": "You can now look things up by name in no time.",
    },
    "10": {
        "title": "Machines that make things (functions)",
        "story": (
            "A function is a machine. You give it ingredients, it gives you a product. "
            "Build the machine once and use it as many times as you like."
        ),
        "points": [
            "def add(a, b): builds the machine.",
            "return sends the answer back out.",
            "*args takes many values, **kwargs takes many key=value pairs.",
            "Default values (b=10) make an argument optional.",
            "A variable made inside a function stays inside that function.",
        ],
        "code": (
            "def add(a, b=10):\n"
            "    return a + b\n"
            "\n"
            "print(add(5))      # 15 (b is 10 by default)\n"
            "print(add(5, 2))   # 7"
        ),
        "win": "You can now build a machine once and reuse it forever.",
    },
    "11": {
        "title": "One line magic (comprehensions)",
        "story": (
            "Sometimes you build a list with a for loop inside the square brackets. "
            "That short cut is called a list comprehension. It is like writing a whole "
            "sentence in one breath."
        ),
        "points": [
            "[x * 2 for x in range(5)] builds a list in one line.",
            "[x for x in data if x > 0] keeps only what matches.",
            "{k: v for ...} builds a dictionary.",
            "any() asks \"is at least one good?\", all() asks \"are all good?\".",
            "A generator uses round brackets and gives items one by one.",
        ],
        "code": (
            "squares = [n * n for n in range(5)]\n"
            "print(squares)\n"
            "big = [n for n in squares if n > 5]\n"
            "print(big)"
        ),
        "win": "You can now build lists faster and shorter.",
    },
    "12": {
        "title": "Notebooks and walls (files & errors)",
        "story": (
            "Files are like notebooks saved on your computer. Errors are your program "
            "hitting a wall. With try and except you can climb over the wall and keep going."
        ),
        "points": [
            "open(\"a.txt\", \"r\") reads, \"w\" writes (and wipes!), \"a\" adds.",
            "with open(...) as f: closes the file for you automatically.",
            "try / except catches errors so the program keeps running.",
            "raise ValueError(\"...\") stops with your own message.",
            "json.dump and json.load work with .json files.",
        ],
        "code": (
            "try:\n"
            "    n = int(\"hello\")\n"
            "except ValueError:\n"
            "    print(\"That was not a number!\")"
        ),
        "win": "You can now save data and survive mistakes.",
    },
    "13": {
        "title": "The big toolbox (modules)",
        "story": (
            "Python ships with a huge toolbox of ready made tools. A module is one box "
            "in that toolbox. You do not need to build the tools yourself, just open the box."
        ),
        "points": [
            "import math then math.sqrt(16).",
            "from math import sqrt lets you use sqrt directly.",
            "pip install <package> adds new tools from the internet.",
            "datetime, random, pathlib and os are already inside.",
            "You can write your own tool in a .py file and import it.",
        ],
        "code": (
            "import math\n"
            "import random\n"
            "\n"
            "print(math.sqrt(16))\n"
            "print(random.randint(1, 6))   # like a dice roll"
        ),
        "win": "You can now use ready made tools instead of building them.",
    },
    "14": {
        "title": "Blueprints and toys (OOP)",
        "story": (
            "A class is a blueprint for a toy. Dog is the blueprint, and your dog Rex is "
            "an object built from that blueprint. Each object gets its own name and age."
        ),
        "points": [
            "class Dog: makes the blueprint.",
            "__init__ sets the starting values of each object.",
            "self means \"this particular dog\".",
            "A method is a function that belongs to the class.",
            "class Puppy(Dog) inherits and reuses everything from Dog.",
        ],
        "code": (
            "class Dog:\n"
            "    def __init__(self, name):\n"
            "        self.name = name\n"
            "\n"
            "    def speak(self):\n"
            "        return self.name + \" says woof\"\n"
            "\n"
            "print(Dog(\"Tommy\").speak())"
        ),
        "win": "You can now build your own objects with their own behaviour.",
    },
    "15": {
        "title": "Taps, lazy lists and magic cloaks",
        "story": (
            "A generator is a tap: it gives you water (items) one glass at a time instead "
            "of filling the whole tank. A decorator is a magic cloak: you put it on a "
            "function and it gains extra powers."
        ),
        "points": [
            "yield turns a function into a generator.",
            "for x in gen: takes the items one by one.",
            "@decorator puts the cloak on your function.",
            "*args and **kwargs let a decorator work with any function.",
            "functools.wraps keeps the original name and doc.",
        ],
        "code": (
            "def counter(n):\n"
            "    for i in range(n):\n"
            "        yield i\n"
            "\n"
            "for x in counter(3):\n"
            "    print(x)"
        ),
        "win": "You can now save memory and add magic to your functions.",
    },
    "16": {
        "title": "Pro toolbox and the robot checker",
        "story": (
            "The standard library is a big professional toolbox, and unittest is a machine "
            "that checks your code for you again and again, so you never break old work."
        ),
        "points": [
            "collections.Counter counts, deque is a super fast queue.",
            "itertools.chain and combinations make loops shorter.",
            "re searches text using patterns.",
            "unittest.TestCase lets you write tests that say PASS or FAIL.",
            "assert checks a condition inside a test.",
        ],
        "code": (
            "from collections import Counter\n"
            "\n"
            "print(Counter(\"aab\").most_common(1))   # [('a', 2)]"
        ),
        "win": "You can now use pro tools and test your own code.",
    },
}
