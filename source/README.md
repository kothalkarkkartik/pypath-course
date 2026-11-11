# Python from Zero to DSA

This is your personal Python course. 17 chapters, and each chapter has:

- **Notes** (at the top of the file, in simple English)
- **Runnable demos** (run them and see the output)
- **Exercises with auto-tests** (solve them yourself, PASS/FAIL shows up right away)
- **Solutions** (only when you need them, with the `--solutions` flag)

Everything runs offline. No internet or account needed.

### Kid mode (for total beginners)

The portal has a **Kid mode** button in the top bar. When it is on, every chapter shows:

- a short story about the topic (robot, school bag, blueprint...)
- 5 very simple points in plain words
- a tiny 5-line program you can run right in the browser

Turn it off with the same button to read the full, detailed notes.

---

## 1. Setup check (1 minute)

Open a terminal (PowerShell) and type:

```powershell
python --version
```

You should see `Python 3.12.x`. If you get "not found", close the terminal and open a new one (so the PATH updates).

If Python is not installed at all:

```powershell
winget install -e --id Python.Python.3.12 --scope user
```

If you want to use VS Code, install the extension: **Python** (by Microsoft).

---

## 2. Course structure

```text
Default Project/
├── practice.py              <- Start here every day (menu app)
├── quiz_bank.py             <- 50 rapid-fire questions
├── cheatsheet.md            <- One-page revision notes
├── progress.json            <- Your progress (created automatically)
├── chapters/
│   ├── _kit.py              <- helper (do not touch this)
│   ├── 00_absolute_basics.py <- START HERE if you are a complete beginner
│   ├── 01_setup_basics.py
│   ├── 02_variables_types.py
│   ├── 03_operators.py
│   ├── 04_strings.py
│   ├── 05_conditionals.py
│   ├── 06_loops.py
│   ├── 07_lists.py
│   ├── 08_tuples_sets.py
│   ├── 09_dicts.py
│   ├── 10_functions.py
│   ├── 11_comprehensions.py
│   ├── 12_files_exceptions.py
│   ├── 13_modules.py
│   ├── 14_oop.py
│   ├── 15_advanced.py
│   └── 16_stdlib_testing.py
├── projects/
│   ├── 01_number_guessing.py
│   ├── 02_todo_cli.py
│   └── 03_expense_tracker.py
└── dsa/
    ├── 00_roadmap.md        <- The plan after Python
    └── 01_patterns_starter.py
```

---

## 3. How to study every day (45-60 min)

```powershell
cd "C:\Users\user\Documents\Default Project"
python practice.py
```

Press **1** in the menu -> today's next chapter opens.

A chapter routine:

| Step | Time | What to do |
|------|------|----------------|
| 1 | 5 min | Read the notes at the top of the file |
| 2 | 10 min | Run the demos, understand the output, change the code and experiment |
| 3 | 25 min | Fill in the exercise `TODO`s yourself, then run the file again |
| 4 | 5 min | Check your answers with `--solutions` |
| 5 | 5 min | Revise that topic in `cheatsheet.md` |

**Rule:** Only count a chapter as complete when all exercises **PASS** (zero pending/fail).

You can also run a file directly:

```powershell
python chapters\04_strings.py
python chapters\04_strings.py --solutions
```

---

## 4. 20-Day Plan

| Day | Chapter | Topic |
|-----|---------|-------|
| 1 | 00 + 01 | Absolute basics, setup, print, comments, input, errors |
| 2 | 02 | Variables, types, conversion, f-strings |
| 3 | 03 | Operators, %, //, logic, precedence |
| 4 | 04 | Strings, slicing, split/join, methods |
| 5 | 05 | if/elif/else, ternary, match-case |
| 6 | 06 | for, while, break/continue, patterns |
| 7 | Revision | Quiz + **Project 1: Number Guessing** |
| 8 | 07 | Lists, sorting, copy vs alias |
| 9 | 08 | Tuples, sets, set operations |
| 10 | 09 | Dicts, counting, grouping, sorting |
| 11 | 10 | Functions, *args, **kwargs, scope |
| 12 | 11 | Comprehensions, generators, any/all |
| 13 | 12 | Files, JSON, try/except, raise |
| 14 | 13 | Modules, pip, venv, datetime, pathlib |
| 15 | 14 | OOP: class, inheritance, dunder |
| 16 | 15 | Iterators, generators, decorators |
| 17 | 16 | collections, itertools, re, unittest |
| 18 | Revision | Quiz + **Project 2: Todo CLI** |
| 19 | Practice | **Project 3: Expense Tracker** + make changes in your own project |
| 20 | Final | Quiz on all chapters, start the DSA roadmap |

If you miss a day, no worries. The app tracks your streak on its own - just come back the next day.

---

## 5. Projects

```powershell
python projects\01_number_guessing.py
python projects\02_todo_cli.py
python projects\03_expense_tracker.py
```

- **01 Number Guessing** - random, while loop, input validation
- **02 Todo CLI** - list of dicts + JSON persistence
- **03 Expense Tracker** - grouping, summary, CSV export

Change the projects: add new features (priority, due date, budget limit, edit option). That is where real learning happens.

---

## 6. Progress and streak

- When you complete a chapter, the app saves it in `progress.json`.
- Press **4** in the menu to see your progress.
- You can reset with **6**.
- Opening the app every day increases your streak.

---

## 7. Common errors (a table worth remembering)

| Error | Meaning | Fix |
|-------|--------|-----|
| `SyntaxError` | The code structure is wrong | Missing `:`, bracket or quote |
| `IndentationError` | Wrong spacing | 4 spaces inside a block |
| `NameError` | Variable not found | Check the spelling, define it first |
| `TypeError` | Wrong type | Convert with `int()` / `str()` |
| `ValueError` | Type is fine, value is wrong | Cases like `int("abc")` |
| `IndexError` | Index out of range | Check with `len()` |
| `KeyError` | Dict key not found | Use `.get()` |
| `AttributeError` | Wrong method/attribute | Check the spelling / type |
| `ZeroDivisionError` | Dividing by 0 | Check before dividing |
| `ModuleNotFoundError` | Package is not installed | `pip install <name>` |

The golden rule of debugging: **read the last line of the traceback first.**

---

## 8. DSA after Python

The full DSA core is built as 16 runnable chapters in `dsa/`:

```text
dsa/
├── _dsa_kit.py            <- helper (do not touch this)
├── d01_patterns.py        <- patterns with loops
├── d02_arrays.py          <- arrays and searching
├── d03_strings.py         <- string algorithms
├── d04_two_pointers.py    <- two pointers
├── d05_sliding_window.py  <- sliding window
├── d06_sorting_searching.py <- sorting + binary search
├── d07_hashing.py         <- hashing, dicts, sets
├── d08_stacks.py          <- stacks
├── d09_queues.py          <- queues and deques
├── d10_linked_list.py     <- linked lists
├── d11_recursion.py       <- recursion and backtracking
├── d12_trees.py           <- trees and BST
├── d13_heaps.py           <- heaps and priority queues
├── d14_graphs.py          <- graphs, BFS, DFS
├── d15_dynamic_programming.py <- dynamic programming
└── d16_binary_search_answers.py <- binary search on the answer
```

Each DSA chapter works exactly like the Python chapters: notes on top, runnable
demos, exercises with auto-tests, and solutions hidden behind `--solutions`.

```powershell
python dsa\d01_patterns.py
python dsa\d01_patterns.py --solutions
```

Or use the practice app: press **6** for the DSA chapter list.

The portal has them too: open **DSA Roadmap** in the portal and click any
chapter. `dsa/00_roadmap.md` still has the 12-week study plan - use it to
spread these 16 chapters over 12 weeks.

For now, do not start DSA. First make loops, lists, dicts and functions solid.
That is the foundation of DSA.

---

## 9. The web portal (HTML + CSS + JS)

```powershell
cd "C:\Users\user\Documents\Default Project\portal"
python -m http.server 8766
```

Open **http://127.0.0.1:8766/**

The portal has two separate courses in the sidebar:

| Python course | DSA course |
|---------------|------------|
| Dashboard | DSA Course (16 chapters) |
| Python Chapters (17) | DSA Quiz (40 questions) |
| Python Projects (3) | DSA Cheatsheet (all templates) |
| Python Quiz (50 questions) | |
| Python Cheatsheet | |
| Python Playground (run code in the browser) | |
| **Practice Game** (26 puzzles, score + streak) | |

Every chapter has: kid-mode notes, full notes, runnable demos, exercises with
expected output, and solutions that stay hidden until you ask for them.

### Practice game

Open **Practice Game** in the sidebar (or press **7** in the terminal app).

- 26 puzzles: Python basics on level 1, real problems on level 2 and 3
- Write the code, press **Check my answer** - the game runs it in your browser
- 10 points for a first-try answer, 5 points if you needed a second try
- Hint and solution buttons (the solution gives no points)
- Your best score and total solved are saved in the browser

If you change any course content, rebuild the portal data:

```powershell
python portal\build_portal.py
```

---

## 10. Things to remember

1. **Do not look at the solutions first.** Struggle on your own for 20 minutes, then look.
2. **Do not copy-paste code.** Type it yourself, make mistakes, fix them.
3. **A little every day.** 45 minutes daily is better than 3 hours on Sunday.
4. **Predict the output** before running. That is the real interview skill.
5. **Do not fear errors.** An error means Python is telling you what is wrong.

All the best. Stay consistent, and you will know Python in 20 days.
