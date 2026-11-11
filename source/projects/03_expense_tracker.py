"""
Project 3 - Expense Tracker
===========================

Add your daily expenses, see the total and a category-wise report,
and export everything to CSV.

Features:
  1. Add an expense (amount, category, note)
  2. List all expenses
  3. Total
  4. Category-wise summary
  5. Delete
  6. CSV export

Concepts: JSON persistence, datetime, dict grouping, CSV, sorting.

Run: python projects/03_expense_tracker.py
"""

import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

DATA_FILE = Path(__file__).parent / "expenses.json"
CSV_FILE = Path(__file__).parent / "expenses.csv"


def load_expenses() -> list:
    if not DATA_FILE.exists():
        return []
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("Warning: expenses.json is damaged, starting with an empty list.")
        return []
    return data if isinstance(data, list) else []


def save_expenses(expenses: list) -> None:
    DATA_FILE.write_text(
        json.dumps(expenses, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def add_expense(expenses: list, amount: float, category: str, note: str) -> None:
    expenses.append({
        "amount": round(amount, 2),
        "category": category,
        "note": note,
        "date": date.today().isoformat(),
    })
    save_expenses(expenses)
    print(f"Added: {amount:.2f} ({category})")


def show_expenses(expenses: list) -> None:
    if not expenses:
        print("There are no expenses yet.")
        return

    print("\n--- EXPENSES ---")
    for i, item in enumerate(expenses, start=1):
        print(f"{i:>3}. {item['date']} | {item['amount']:>8.2f} | "
              f"{item['category']:<12} | {item['note']}")
    print("----------------")
    print(f"Total: {sum(e['amount'] for e in expenses):.2f}")


def show_summary(expenses: list) -> None:
    if not expenses:
        print("Add an expense first to see a summary.")
        return

    by_category = defaultdict(float)
    for item in expenses:
        by_category[item["category"]] += item["amount"]

    total = sum(by_category.values())
    print("\n--- CATEGORY SUMMARY ---")
    for category, amount in sorted(by_category.items(), key=lambda kv: -kv[1]):
        percent = amount / total * 100
        bar = "#" * int(percent / 5)
        print(f"{category:<12} {amount:>9.2f}  {percent:>5.1f}% {bar}")
    print(f"{'TOTAL':<12} {total:>9.2f}")


def delete_expense(expenses: list, index: int) -> None:
    if 1 <= index <= len(expenses):
        removed = expenses.pop(index - 1)
        save_expenses(expenses)
        print(f"Deleted: {removed['amount']:.2f} ({removed['category']})")
    else:
        print("Wrong number.")


def export_csv(expenses: list) -> None:
    if not expenses:
        print("There is no data to export.")
        return

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "amount", "category", "note"])
        writer.writeheader()
        writer.writerows(expenses)

    print(f"CSV exported: {CSV_FILE}")


def main() -> None:
    expenses = load_expenses()
    print("=" * 44)
    print("EXPENSE TRACKER")
    print("=" * 44)

    while True:
        print("\n1. Add  2. List  3. Summary  4. Delete  5. Export CSV  0. Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            raw = input("Amount: ").strip()
            try:
                amount = float(raw)
            except ValueError:
                print("Please enter a valid number.")
                continue
            if amount <= 0:
                print("The amount must be positive.")
                continue

            category = input("Category (food/travel/shopping/other): ").strip() or "other"
            note = input("Note (optional): ").strip()
            add_expense(expenses, amount, category.lower(), note)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            show_summary(expenses)
        elif choice == "4":
            show_expenses(expenses)
            raw = input("Delete number: ").strip()
            if raw.isdigit():
                delete_expense(expenses, int(raw))
            else:
                print("Please enter a number.")
        elif choice == "5":
            export_csv(expenses)
        elif choice == "0":
            print("Bye! Keep saving your money.")
            break
        else:
            print("Please choose 1-5 or 0.")


if __name__ == "__main__":
    main()
