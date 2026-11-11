"""
Project 1 - Number Guessing Game
================================

The computer thinks of a random number (1-100).
You guess, and the computer tells you: too high or too low.
Try to guess it in as few attempts as possible.

Concepts: random, while loop, input, int conversion, try/except, functions.

Run: python projects/01_number_guessing.py
"""

import random


def play_round(low: int = 1, high: int = 100) -> int:
    """Play one round and return the number of attempts."""
    secret = random.randint(low, high)
    attempts = 0

    print(f"\nI'm thinking of a number between {low} and {high}.")
    while True:
        raw = input("Your guess (q = quit): ").strip()
        if raw.lower() == "q":
            print(f"Okay, the number was: {secret}")
            return attempts

        try:
            guess = int(raw)
        except ValueError:
            print("Please enter a number, not text.")
            continue

        if not low <= guess <= high:
            print(f"Please enter a number between {low} and {high}.")
            continue

        attempts += 1

        if guess < secret:
            print("Too low! Try a bigger number.")
        elif guess > secret:
            print("Too high! Try a smaller number.")
        else:
            print(f"Correct! You guessed it in {attempts} attempts.")
            return attempts


def main() -> None:
    print("=" * 40)
    print("NUMBER GUESSING GAME")
    print("=" * 40)

    best = None
    while True:
        attempts = play_round()
        if attempts and (best is None or attempts < best):
            best = attempts
            print(f"New best score: {best} attempts")

        again = input("\nPlay another round? (y/n): ").strip().lower()
        if again != "y":
            break

    print("Thanks for playing!")


if __name__ == "__main__":
    main()
