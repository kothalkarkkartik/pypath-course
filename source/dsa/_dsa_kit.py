"""
_dsa_kit.py - Helper for the DSA chapters. You do not need to edit this.

It simply reuses the same harness as the Python course chapters, so every
DSA file can be run the same way:

  python dsa/d01_patterns.py               <- run the demos + exercises
  python dsa/d01_patterns.py --solutions   <- also print the solutions
"""

import sys
from pathlib import Path

CHAPTERS_DIR = Path(__file__).resolve().parent.parent / "chapters"

if str(CHAPTERS_DIR) not in sys.path:
    sys.path.insert(0, str(CHAPTERS_DIR))

from _kit import demo, main, run_exercises, section  # noqa: E402

__all__ = ["demo", "main", "run_exercises", "section"]
