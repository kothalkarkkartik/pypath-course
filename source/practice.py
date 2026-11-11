"""
practice.py - Your daily practice app
=====================================

Run it:
  python practice.py

It has:
  1. Run today's chapter (next incomplete)
  2. Run any chapter (with or without solutions)
  3. Quiz (10 random questions)
  4. View progress
  5. Run projects

Progress is saved in progress.json.
"""

import json
import random
import subprocess
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHAPTERS_DIR = ROOT / "chapters"
DSA_DIR = ROOT / "dsa"
PROJECTS_DIR = ROOT / "projects"
PROGRESS_FILE = ROOT / "progress.json"

sys.path.insert(0, str(ROOT))
import game_bank  # noqa: E402
import quiz_bank  # noqa: E402


# ---------------------------------------------------------------------------
# Progress file
# ---------------------------------------------------------------------------


def load_progress() -> dict:
    default = {
        "completed": [],
        "dsa_completed": [],
        "game_best": 0,
        "game_solved": 0,
        "quiz_total": 0,
        "quiz_correct": 0,
        "streak": 0,
        "last_day": None,
    }
    if not PROGRESS_FILE.exists():
        return default
    try:
        data = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        default.update(data)
    except (json.JSONDecodeError, OSError):
        print("Warning: could not read progress.json, so a new progress file will be created.")
    return default


def save_progress(progress: dict) -> None:
    PROGRESS_FILE.write_text(
        json.dumps(progress, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def update_streak(progress: dict) -> None:
    today = date.today()
    last = progress.get("last_day")

    if last == today.isoformat():
        return
    if last == (today - timedelta(days=1)).isoformat():
        progress["streak"] = progress.get("streak", 0) + 1
    else:
        progress["streak"] = 1

    progress["last_day"] = today.isoformat()
    save_progress(progress)


# ---------------------------------------------------------------------------
# Chapters
# ---------------------------------------------------------------------------


def get_chapters() -> list[Path]:
    return sorted(CHAPTERS_DIR.glob("[0-9][0-9]_*.py"))


def chapter_title(path: Path) -> str:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return path.stem
    if len(lines) > 1 and lines[0].strip() == '"""':
        return lines[1].strip()
    return path.stem


def chapter_number(path: Path) -> str:
    return path.name[:2]


def get_dsa_chapters() -> list[Path]:
    return sorted(DSA_DIR.glob("d[0-9][0-9]_*.py"))


def dsa_chapter_number(path: Path) -> str:
    return path.name[1:3]


def show_dsa_chapters(progress: dict) -> list[Path]:
    chapters = get_dsa_chapters()
    done_list = progress.get("dsa_completed", [])
    print("\n--- DSA CHAPTERS ---")
    for index, path in enumerate(chapters, start=1):
        done = "[x]" if dsa_chapter_number(path) in done_list else "[ ]"
        print(f" {done} {index:>2}. {chapter_title(path)}")
    print("---------------------")
    return chapters


def run_dsa_chapter(path: Path, progress: dict, show_solutions: bool = False) -> None:
    command = [sys.executable, str(path)]
    if show_solutions:
        command.append("--solutions")

    print(f"\nRunning: {path.name}")
    if show_solutions:
        print("(solutions mode: try it yourself first!)")
    print("-" * 64)

    try:
        subprocess.call(command, cwd=ROOT)
    except KeyboardInterrupt:
        print("\nChapter stopped.")
        return

    number = dsa_chapter_number(path)
    done_list = progress.setdefault("dsa_completed", [])
    if number in done_list:
        return

    answer = input("\nChapter finished? Mark it complete (y/n): ").strip().lower()
    if answer == "y":
        done_list.append(number)
        save_progress(progress)
        print(f"DSA chapter {number} marked as complete!")


def choose_and_run_dsa(progress: dict) -> None:
    chapters = show_dsa_chapters(progress)
    if not chapters:
        print("No DSA chapters found.")
        return

    raw = input("\nChapter number (0 = back): ").strip()
    if not raw.isdigit():
        return
    index = int(raw)
    if index == 0:
        return
    if not 1 <= index <= len(chapters):
        print("Invalid number.")
        return

    path = chapters[index - 1]
    mode = input("1 = normal, 2 = show solutions (1/2): ").strip()
    run_dsa_chapter(path, progress, show_solutions=(mode == "2"))


def show_chapters(progress: dict) -> list[Path]:
    chapters = get_chapters()
    print("\n--- CHAPTERS ---")
    for index, path in enumerate(chapters, start=1):
        done = "[x]" if chapter_number(path) in progress["completed"] else "[ ]"
        print(f" {done} {index:>2}. {chapter_title(path)}")
    print("----------------")
    return chapters


def run_chapter(path: Path, progress: dict, show_solutions: bool = False) -> None:
    command = [sys.executable, str(path)]
    if show_solutions:
        command.append("--solutions")

    print(f"\nRunning: {path.name}")
    if show_solutions:
        print("(solutions mode: try it yourself first!)")
    print("-" * 64)

    try:
        subprocess.call(command, cwd=ROOT)
    except KeyboardInterrupt:
        print("\nChapter stopped.")
        return

    number = chapter_number(path)
    if number in progress["completed"]:
        return

    answer = input("\nChapter finished? Mark it complete (y/n): ").strip().lower()
    if answer == "y":
        progress["completed"].append(number)
        save_progress(progress)
        print(f"Chapter {number} marked as complete!")


def choose_and_run(progress: dict) -> None:
    chapters = show_chapters(progress)
    if not chapters:
        print("No chapters found.")
        return

    raw = input("\nChapter number (0 = back): ").strip()
    if not raw.isdigit():
        return
    index = int(raw)
    if index == 0:
        return
    if not 1 <= index <= len(chapters):
        print("Invalid number.")
        return

    path = chapters[index - 1]
    mode = input("1 = normal, 2 = show solutions (1/2): ").strip()
    run_chapter(path, progress, show_solutions=(mode == "2"))


def run_next(progress: dict) -> None:
    pending = [p for p in get_chapters() if chapter_number(p) not in progress["completed"]]
    if not pending:
        print("\nAll chapters complete! Now build the projects and start DSA.")
        print("See: dsa/00_roadmap.md")
        return

    path = pending[0]
    print(f"\nToday's chapter: {chapter_title(path)}")
    run_chapter(path, progress)


# ---------------------------------------------------------------------------
# Quiz
# ---------------------------------------------------------------------------


def run_quiz(progress: dict) -> None:
    total_questions = len(quiz_bank.QUESTIONS)
    count = min(10, total_questions)
    questions = random.sample(quiz_bank.QUESTIONS, count)

    print(f"\n--- QUIZ ({count} questions) ---")
    score = 0
    attempted = 0

    for number, question in enumerate(questions, start=1):
        print(f"\nQ{number}. {question['q']}")
        for option_number, option in enumerate(question["options"], start=1):
            print(f"   {option_number}. {option}")

        raw = input("Answer (1-4, q = quit): ").strip().lower()
        if raw == "q":
            print("Quiz exited.")
            break
        if not raw.isdigit() or not 1 <= int(raw) <= len(question["options"]):
            print("Invalid option, skipping.")
            continue

        attempted += 1
        chosen = int(raw) - 1
        if chosen == question["answer"]:
            score += 1
            print("Correct!")
        else:
            print(f"Wrong. The correct answer is: {question['options'][question['answer']]}")
        print(f"Why: {question['explain']}")

    if attempted == 0:
        return

    progress["quiz_total"] += attempted
    progress["quiz_correct"] += score
    save_progress(progress)

    print(f"\nScore: {score}/{attempted}")
    if score == attempted:
        print("Perfect! Today's revision is solid.")
    elif score >= attempted * 0.7:
        print("Good job. Read up again on the topics you missed.")
    else:
        print("Do a little revision, then try the quiz again.")


# ---------------------------------------------------------------------------
# Practice game
# ---------------------------------------------------------------------------


def run_python_code(code: str) -> tuple[str, str, bool]:
    """Run a piece of Python code and return (stdout, stderr, ok)."""
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "game_check.py"
        path.write_text(code, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(path)],
            capture_output=True,
            text=True,
            cwd=folder,
        )
        return result.stdout or "", result.stderr or "", result.returncode == 0


def read_code_block() -> str:
    """Read lines from the user until an empty line."""
    print("(type your code, then press Enter on an empty line)")
    lines: list[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "" and lines:
            break
        lines.append(line)
    return "\n".join(lines)


def run_game(progress: dict) -> None:
    puzzles = random.sample(game_bank.PUZZLES, min(10, len(game_bank.PUZZLES)))
    score = 0
    streak = 0

    print("\n--- PRACTICE GAME ---")
    print(f"{len(puzzles)} puzzles, 10 points for a first-try answer.")

    for number, puzzle in enumerate(puzzles, start=1):
        print("\n" + "=" * 56)
        print(f" PUZZLE {number}/{len(puzzles)}  [{puzzle['tag']} - level {puzzle['level']}]")
        print("=" * 56)
        print(puzzle["title"])
        print()
        print(puzzle["story"])
        print()
        print("Starter code:")
        print(puzzle["starter"])

        code = read_code_block()
        full = code + ("\n\n" + puzzle["test"] if puzzle.get("test") else "")
        stdout, stderr, ok = run_python_code(full)
        got = stdout.strip()
        expected = puzzle["expected"].strip()

        if ok and got == expected:
            score += 10
            streak += 1
            print(f"\nCORRECT! +10 points. Streak: {streak}")
        else:
            streak = 0
            print("\nNot quite.")
            if stderr.strip():
                print("Your code gave an error:")
                print(stderr.strip()[:400])
            else:
                print("Your output was:")
                print(got or "(nothing)")
                print("Expected:")
                print(expected)

            show = input("\nSee the solution? (y/n): ").strip().lower()
            if show == "y":
                print("\n--- SOLUTION ---")
                print(puzzle["solution"])
                print("---")
                print("Hint for next time:", puzzle["hint"])

        progress["game_best"] = max(progress.get("game_best", 0), score)
        progress["game_solved"] = progress.get("game_solved", 0) + (1 if ok and got == expected else 0)
        save_progress(progress)

    print("\n" + "=" * 56)
    print(f" FINAL SCORE: {score}")
    print(f" Best score ever: {progress.get('game_best', 0)}")
    print("=" * 56)


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------


def run_project(progress: dict) -> None:
    projects = sorted(PROJECTS_DIR.glob("*.py"))
    if not projects:
        print("No projects found.")
        return

    print("\n--- PROJECTS ---")
    for index, path in enumerate(projects, start=1):
        print(f" {index}. {path.name}")
    print("----------------")

    raw = input("Project number (0 = back): ").strip()
    if not raw.isdigit():
        return
    index = int(raw)
    if index == 0:
        return
    if not 1 <= index <= len(projects):
        print("Invalid number.")
        return

    try:
        subprocess.call([sys.executable, str(projects[index - 1])], cwd=ROOT)
    except KeyboardInterrupt:
        print("\nProject stopped.")


# ---------------------------------------------------------------------------
# Progress view
# ---------------------------------------------------------------------------


def show_progress(progress: dict) -> None:
    chapters = get_chapters()
    completed = [c for c in chapters if chapter_number(c) in progress["completed"]]
    percent = len(completed) / len(chapters) * 100 if chapters else 0

    print("\n--- YOUR PROGRESS ---")
    print(f"Chapters : {len(completed)}/{len(chapters)} ({percent:.0f}%)")
    bar = "#" * int(percent / 5)
    print(f"Progress : [{bar:<20}]")

    if progress["quiz_total"]:
        accuracy = progress["quiz_correct"] / progress["quiz_total"] * 100
        print(f"Quiz     : {progress['quiz_correct']}/{progress['quiz_total']} "
              f"({accuracy:.0f}% accuracy)")
    else:
        print("Quiz     : no quizzes yet")

    print(f"Streak   : {progress['streak']} day(s)")

    pending = [chapter_title(c) for c in chapters if c not in completed]
    if pending:
        print("\nNext up:")
        for title in pending[:3]:
            print("  -", title)
    print("------------------------")


def reset_progress(progress: dict) -> None:
    answer = input("Are you sure you want to reset? (yes/n): ").strip().lower()
    if answer == "yes":
        progress.clear()
        progress.update({
            "completed": [],
            "dsa_completed": [],
            "game_best": 0,
            "game_solved": 0,
            "quiz_total": 0,
            "quiz_correct": 0,
            "streak": 0,
            "last_day": None,
        })
        save_progress(progress)
        print("Progress reset.")


# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------


def main() -> None:
    progress = load_progress()
    update_streak(progress)

    while True:
        print("\n" + "=" * 56)
        print(" PYTHON + DSA PRACTICE APP")
        print("=" * 56)
        print(" 1. Run today's chapter (next incomplete)")
        print(" 2. Chapter list / run any chapter")
        print(" 3. Quiz (10 random questions)")
        print(" 4. View progress")
        print(" 5. Run projects")
        print(" 6. DSA chapters (patterns to DP)")
        print(" 7. Practice game (10 puzzles)")
        print(" 8. Reset progress")
        print(" 0. Exit")
        print("-" * 56)
        print(f" Streak: {progress['streak']} day(s) | "
              f"Python: {len(progress['completed'])}/{len(get_chapters())} | "
              f"DSA: {len(progress.get('dsa_completed', []))}/{len(get_dsa_chapters())}")

        try:
            choice = input("\nChoice: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        try:
            if choice == "1":
                run_next(progress)
            elif choice == "2":
                choose_and_run(progress)
            elif choice == "3":
                run_quiz(progress)
            elif choice == "4":
                show_progress(progress)
            elif choice == "5":
                run_project(progress)
            elif choice == "6":
                choose_and_run_dsa(progress)
            elif choice == "7":
                run_game(progress)
            elif choice == "8":
                reset_progress(progress)
            elif choice == "0":
                print("You're done for today. Come back tomorrow!")
                break
            else:
                print("Please choose a number from 0 to 6.")
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break


if __name__ == "__main__":
    main()
