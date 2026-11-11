"""
Portal builder - builds the portal data from the chapter files.
===============================================================

Run:
  python portal/build_portal.py

This reads content from chapters/*.py, projects/*.py, quiz_bank.py, cheatsheet.md
and dsa/, and creates portal/assets/data.js.
Whenever you change the course content, run this script again.
"""

from __future__ import annotations

import ast
import importlib.util
import inspect
import json
import re
import sys
import textwrap
import time
from pathlib import Path

PORTAL_DIR = Path(__file__).resolve().parent
ROOT = PORTAL_DIR.parent
CHAPTERS_DIR = ROOT / "chapters"
DSA_DIR = ROOT / "dsa"
PROJECTS_DIR = ROOT / "projects"
ASSETS_DIR = PORTAL_DIR / "assets"

sys.path.insert(0, str(CHAPTERS_DIR))
sys.path.insert(0, str(DSA_DIR))
sys.path.insert(0, str(ROOT))

import kid_lessons  # noqa: E402  (needs the path above)
import kid_lessons_dsa  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def load_module(path: Path):
    name = f"portal_{path.stem}"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Module did not load: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def doc_to_md(doc: str) -> str:
    """Turn a docstring into markdown.

    It puts indented code lines inside ```python fences, and turns short
    'Heading:' style lines into ### headings.
    """
    lines = doc.strip("\n").splitlines()

    # The first line is the title, the second is an underline (=====) - drop both
    if len(lines) >= 2 and lines[0].strip() and lines[1].strip():
        if set(lines[1].strip()) <= {"="}:
            lines = lines[2:]

    output: list[str] = []
    in_code = False

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        is_list = bool(re.match(r"^\s*([-*]|\d+\.)\s+", line))
        is_code = (
            stripped
            and not is_list
            and (line.startswith("  ") or line.startswith("\t"))
        )

        if is_code and not in_code:
            output.append("```python")
            in_code = True
        elif not is_code and in_code:
            output.append("```")
            in_code = False

        if (
            not is_code
            and not in_code
            and stripped.endswith(":")
            and len(stripped) < 70
            and not is_list
            and not stripped.startswith("#")
        ):
            output.append(f"### {stripped}")
        else:
            output.append(line)

    if in_code:
        output.append("```")

    return "\n".join(output).strip()


def preview_value(value) -> str:
    if callable(value):
        return "fn"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    return repr(value)


def tests_preview(exercise: dict, display_name: str) -> list[str]:
    rows = []
    for args, expected in exercise["tests"]:
        inside = ", ".join(preview_value(arg) for arg in args)
        rows.append(f"{display_name}({inside})  ->  {preview_value(expected)}")
    return rows


def clean_source(obj) -> str:
    try:
        return textwrap.dedent(inspect.getsource(obj)).strip()
    except (OSError, TypeError):
        return ""


def first_line(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return fallback


def module_preamble(module) -> str:
    """Module-level imports and constants that the demo code needs.

    A demo function runs alone in the browser, so its imports and simple
    constants (like MONTHS) have to be sent along with it. The _kit import
    is skipped because it isn't available in the portal.
    """
    try:
        source = inspect.getsource(module)
    except (OSError, TypeError):
        return ""

    tree = ast.parse(source)
    chunks = []

    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            segment = ast.get_source_segment(source, node) or ""
            if "_kit" in segment:
                continue
            chunks.append(segment)
        elif isinstance(node, ast.Assign):
            names = [t.id for t in node.targets if isinstance(t, ast.Name)]
            if names and all(name in ("EXERCISES", "DEMOS") for name in names):
                continue
            segment = ast.get_source_segment(source, node)
            if segment:
                chunks.append(segment)
        elif isinstance(node, ast.AnnAssign):
            segment = ast.get_source_segment(source, node)
            if segment:
                chunks.append(segment)

    return "\n".join(chunks)


# ---------------------------------------------------------------------------
# Chapters
# ---------------------------------------------------------------------------


def extract_chapter(module, path: Path, num: str, file_label: str, kid: dict | None) -> dict:
    """Turn one chapter module into the dict the portal understands."""
    doc = inspect.getdoc(module) or ""
    title = first_line(doc, path.stem)
    notes = doc_to_md(doc)

    preamble = module_preamble(module)

    demos = []
    for demo_title, demo_func in module.DEMOS:
        body = clean_source(demo_func)
        call = f"{demo_func.__name__}()"
        code = f"{preamble}\n\n\n{body}\n\n\n{call}" if preamble else f"{body}\n\n\n{call}"
        demos.append({
            "title": demo_title,
            "code": code,
        })

    exercises = []
    for exercise in module.EXERCISES:
        starter_obj = exercise["func"]
        if exercise.get("starter_name"):
            starter_obj = getattr(module, exercise["starter_name"], starter_obj)

        solution_obj = exercise["solution"]
        if exercise.get("solution_name"):
            solution_obj = getattr(module, exercise["solution_name"], solution_obj)

        display_name = (
            exercise.get("starter_name")
            or getattr(exercise["func"], "__name__", "function")
        )

        exercises.append({
            "id": exercise["id"],
            "task": exercise["task"],
            "tests": tests_preview(exercise, display_name),
            "starter": clean_source(starter_obj),
            "solution": clean_source(solution_obj),
        })

    return {
        "num": num,
        "title": title,
        "file": file_label,
        "notes": notes,
        "kid": kid,
        "demos": demos,
        "exercises": exercises,
        "minutes": 35 + len(exercises) * 3,
    }


def build_chapters() -> list[dict]:
    chapters = []

    for path in sorted(CHAPTERS_DIR.glob("[0-9][0-9]_*.py")):
        module = load_module(path)
        chapters.append(
            extract_chapter(
                module,
                path,
                num=path.name[:2],
                file_label=f"chapters/{path.name}",
                kid=kid_lessons.LESSONS.get(path.name[:2]),
            )
        )

    return chapters


def build_dsa_chapters() -> list[dict]:
    chapters = []

    for path in sorted(DSA_DIR.glob("d[0-9][0-9]_*.py")):
        module = load_module(path)
        num = "D" + path.name[1:3]
        chapters.append(
            extract_chapter(
                module,
                path,
                num=num,
                file_label=f"dsa/{path.name}",
                kid=kid_lessons_dsa.LESSONS.get(num),
            )
        )

    return chapters


# ---------------------------------------------------------------------------
# Projects, DSA, quiz, cheatsheet
# ---------------------------------------------------------------------------


def build_projects() -> list[dict]:
    projects = []

    for path in sorted(PROJECTS_DIR.glob("*.py")):
        source = path.read_text(encoding="utf-8")
        try:
            doc = ast.get_docstring(ast.parse(source)) or ""
        except SyntaxError:
            doc = ""

        projects.append({
            "file": f"projects/{path.name}",
            "name": path.name,
            "title": first_line(doc, path.stem),
            "notes": doc_to_md(doc),
            "code": source,
        })

    return projects


def build_dsa() -> dict:
    roadmap_path = ROOT / "dsa" / "00_roadmap.md"
    starter_path = ROOT / "dsa" / "01_patterns_starter.py"
    cheatsheet_path = ROOT / "dsa" / "01_cheatsheet.md"

    roadmap = roadmap_path.read_text(encoding="utf-8") if roadmap_path.exists() else ""
    starter_source = starter_path.read_text(encoding="utf-8") if starter_path.exists() else ""
    cheatsheet = (
        cheatsheet_path.read_text(encoding="utf-8") if cheatsheet_path.exists() else ""
    )

    starter_doc = ""
    if starter_source:
        try:
            starter_doc = ast.get_docstring(ast.parse(starter_source)) or ""
        except SyntaxError:
            starter_doc = ""

    return {
        "roadmap": roadmap,
        "cheatsheet": cheatsheet,
        "starter": {
            "title": first_line(starter_doc, "DSA Starter"),
            "notes": doc_to_md(starter_doc),
            "code": starter_source,
            "file": "dsa/01_patterns_starter.py",
        },
    }


def build_quiz() -> list[dict]:
    import quiz_bank

    return quiz_bank.QUESTIONS


def build_dsa_quiz() -> list[dict]:
    try:
        import quiz_bank_dsa
    except ImportError:
        return []

    return quiz_bank_dsa.QUESTIONS


def build_game() -> list[dict]:
    try:
        import game_bank
    except ImportError:
        return []

    return game_bank.PUZZLES


def update_asset_version() -> str:
    """Put a fresh ?v=... on the asset links so browsers never use old files."""
    index_path = PORTAL_DIR / "index.html"
    if not index_path.exists():
        return "0"

    version = str(int(time.time()))
    html = index_path.read_text(encoding="utf-8")

    html = re.sub(r'(assets/(?:style\.css|data\.js|app\.js))(?:\?v=\d+)?', rf"\1?v={version}", html)

    index_path.write_text(html, encoding="utf-8")
    return version


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    chapters = build_chapters()
    dsa_chapters = build_dsa_chapters()
    projects = build_projects()
    dsa = build_dsa()
    quiz = build_quiz()
    dsa_quiz = build_dsa_quiz()
    game = build_game()
    cheatsheet_path = ROOT / "cheatsheet.md"
    cheatsheet = (
        cheatsheet_path.read_text(encoding="utf-8")
        if cheatsheet_path.exists()
        else ""
    )

    data = {
        "meta": {
            "title": "PyPath - Python from Zero to DSA",
            "chapterCount": len(chapters),
            "exerciseCount": sum(len(c["exercises"]) for c in chapters),
            "demoCount": sum(len(c["demos"]) for c in chapters),
            "quizCount": len(quiz),
            "dsaQuizCount": len(dsa_quiz),
            "gameCount": len(game),
            "dsaChapterCount": len(dsa_chapters),
            "dsaExerciseCount": sum(len(c["exercises"]) for c in dsa_chapters),
            "dsaDemoCount": sum(len(c["demos"]) for c in dsa_chapters),
        },
        "chapters": chapters,
        "dsaChapters": dsa_chapters,
        "projects": projects,
        "dsa": dsa,
        "quiz": quiz,
        "dsaQuiz": dsa_quiz,
        "game": game,
        "cheatsheet": cheatsheet,
    }

    output = ASSETS_DIR / "data.js"
    output.write_text(
        "window.PYCOURSE = "
        + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )

    version = update_asset_version()

    size_kb = output.stat().st_size / 1024
    print("Portal data is ready:", output)
    print(f"  Chapters : {len(chapters)}")
    print(f"  Demos    : {data['meta']['demoCount']}")
    print(f"  Exercises: {data['meta']['exerciseCount']}")
    print(f"  Quiz     : {len(quiz)}")
    print(f"  DSA      : {len(dsa_chapters)} chapters, {data['meta']['dsaExerciseCount']} exercises")
    print(f"  Size     : {size_kb:.1f} KB")
    print(f"  Cache    : ?v={version}")


if __name__ == "__main__":
    main()
