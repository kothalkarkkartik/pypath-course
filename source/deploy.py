"""
deploy.py - Publish the portal to GitHub Pages (free).

Run this after changing any course content:

  python deploy.py

What it does:
  1. Rebuilds portal/assets/data.js from the chapter files
  2. Copies the static site (index.html + assets) into a staging folder
  3. Copies the full course source into the repo's source/ folder
  4. Commits and pushes to the GitHub repo
  5. GitHub Pages rebuilds the site (takes about a minute)

Live URL: https://kothalkarkkartik.github.io/pypath-course/
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORTAL_DIR = ROOT / "portal"
REPO = "kothalkarkkartik/pypath-course"
SITE_URL = f"https://{REPO.split('/')[0]}.github.io/{REPO.split('/')[1]}/"

SOURCE_FILES = [
    "practice.py",
    "quiz_bank.py",
    "quiz_bank_dsa.py",
    "game_bank.py",
    "kid_lessons.py",
    "kid_lessons_dsa.py",
    "cheatsheet.md",
    "README.md",
    "deploy.py",
]
SOURCE_DIRS = ["chapters", "dsa", "projects"]


def run(command: list[str], cwd: Path | None = None, allow_fail: bool = False) -> None:
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        if allow_fail:
            return
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(f"Command failed: {' '.join(command)}")


def build_data() -> None:
    print("1. Rebuilding portal data...")
    run([sys.executable, str(PORTAL_DIR / "build_portal.py")], cwd=ROOT)


def stage(folder: Path) -> None:
    print("2. Staging the site...")

    shutil.copy2(PORTAL_DIR / "index.html", folder / "index.html")
    shutil.copytree(PORTAL_DIR / "assets", folder / "assets", dirs_exist_ok=True)

    source = folder / "source"
    source.mkdir(exist_ok=True)

    for name in SOURCE_DIRS:
        target = source / name
        shutil.rmtree(target, ignore_errors=True)
        shutil.copytree(ROOT / name, target, dirs_exist_ok=True)

    for name in SOURCE_FILES:
        path = ROOT / name
        if path.exists():
            shutil.copy2(path, source / name)

    build_script = source / "portal"
    build_script.mkdir(exist_ok=True)
    shutil.copy2(PORTAL_DIR / "build_portal.py", build_script / "build_portal.py")

    (folder / ".gitignore").write_text(
        "__pycache__/\n*.pyc\nprogress.json\n*.tmp\n.DS_Store\n", encoding="utf-8"
    )

    print(f"   {sum(1 for _ in folder.rglob('*') if _.is_file())} files ready")


def push(folder: Path) -> None:
    print("3. Committing and pushing...")

    if not (folder / ".git").exists():
        run(["git", "init", "-b", "main"], cwd=folder)
        run(["git", "config", "user.name", "kothalkarkkartik"], cwd=folder)
        run(
            ["git", "config", "user.email", "kothalkarkkartik@users.noreply.github.com"],
            cwd=folder,
        )

    # the staging folder is new every time, so always (re)set the remote
    run(["git", "remote", "remove", "origin"], cwd=folder, allow_fail=True)
    run(["git", "remote", "add", "origin", f"https://github.com/{REPO}.git"], cwd=folder)

    run(["git", "add", "-A"], cwd=folder)
    run(["git", "commit", "-m", "Update PyPath course content"], cwd=folder)
    # the staging folder is rebuilt from scratch every time, so the history is new:
    # force-push is safe here because the remote holds the same generated content
    run(["git", "push", "--force", "origin", "main"], cwd=folder)


def main() -> None:
    build_data()

    with tempfile.TemporaryDirectory() as temp:
        folder = Path(temp) / "site"
        folder.mkdir()
        stage(folder)
        push(folder)

    print("\nDone.")
    print(f"Live site : {SITE_URL}")
    print(f"Repo      : https://github.com/{REPO}")
    print("GitHub Pages needs about a minute to rebuild.")


if __name__ == "__main__":
    main()
