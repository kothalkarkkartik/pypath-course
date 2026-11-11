"""
_kit.py - A small helper for all chapters. You don't need to edit this file.

Every chapter takes 3 things from it:
  section(title)  -> prints a heading on the screen
  demo(title, fn) -> runs a demo function safely and shows any error
  main(demos, exercises) -> runs the whole chapter (demos + exercises)
"""

from __future__ import annotations

import inspect
import sys
import traceback

LINE = "=" * 64


def section(title: str) -> None:
    print(f"\n{LINE}\n{title}\n{LINE}")


def demo(title: str, fn) -> None:
    section(title)
    try:
        fn()
    except Exception:
        print("!! An error happened in this demo (that's a good thing for learning):")
        traceback.print_exc()


def _print_solution(ex: dict) -> None:
    sol = ex.get("solution")
    if sol is None:
        return
    print("\n  --- SOLUTION (try it yourself first!) ---")
    for line in inspect.getsource(sol).rstrip().splitlines():
        print("  " + line)
    print("  ----------------------------------------")


def run_exercises(exercises: list[dict], show_solutions: bool = False) -> int:
    passed = failed = pending = 0
    print(f"\n{LINE}\nEXERCISES ({len(exercises)})\n{LINE}")
    print("Each function has a TODO inside. Write your code there, then run the file again.")

    for ex in exercises:
        print(f"\n[{ex['id']}] {ex['task']}")
        fn = ex["func"]
        try:
            attempted = True
            for args, expected in ex["tests"]:
                got = fn(*args)
                if got is None and expected is not None:
                    print("  ... not attempted yet (got None back)")
                    attempted = False
                    break
                if got == expected:
                    passed += 1
                    print(f"  PASS {args} -> {got!r}")
                else:
                    failed += 1
                    print(f"  FAIL {args} -> got {got!r}, expected {expected!r}")
            if not attempted:
                pending += 1
        except NotImplementedError:
            pending += 1
            print("  ... TODO still left")
        except Exception as e:
            failed += 1
            print(f"  ERROR: {type(e).__name__}: {e}")

        if show_solutions:
            _print_solution(ex)

    print(f"\n{LINE}")
    print(f"RESULT: {passed} pass, {failed} fail, {pending} pending")
    if failed == 0 and pending == 0:
        print("Well done! Chapter complete. Now open the next chapter with practice.py.")
    else:
        print("Tip: solve it yourself first, then run with `--solutions` to compare.")
    return failed


def main(demos: list[tuple[str, object]], exercises: list[dict]) -> None:
    print("Python Course - chapter practice file")
    print("Run: python <file>.py            (demos + exercises)")
    print("     python <file>.py --solutions (also show the solutions)")
    for title, fn in demos:
        demo(title, fn)
    show = "--solutions" in sys.argv or "-s" in sys.argv
    run_exercises(exercises, show_solutions=show)
