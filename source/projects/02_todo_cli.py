"""
Project 2 - Todo List CLI
=========================

Manage your daily tasks from the terminal. Your data is saved in a JSON file.

Features:
  1. Add a task
  2. Show all tasks
  3. Mark a task as done
  4. Delete a task
  5. Clear everything

Concepts: list of dicts, JSON file, functions, while loop, input validation.

Run: python projects/02_todo_cli.py
"""

import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "todo_data.json"


def load_todos() -> list:
    if not DATA_FILE.exists():
        return []
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("Warning: the data file is damaged, starting with an empty list.")
        return []
    return data if isinstance(data, list) else []


def save_todos(todos: list) -> None:
    DATA_FILE.write_text(
        json.dumps(todos, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def next_id(todos: list) -> int:
    return max((todo["id"] for todo in todos), default=0) + 1


def add_todo(todos: list, text: str) -> None:
    todos.append({"id": next_id(todos), "text": text, "done": False})
    save_todos(todos)
    print(f"Added: {text}")


def show_todos(todos: list) -> None:
    if not todos:
        print("There are no tasks yet. Add one first.")
        return

    print("\n--- YOUR TASKS ---")
    for todo in todos:
        mark = "[x]" if todo["done"] else "[ ]"
        print(f"{todo['id']:>3}. {mark} {todo['text']}")
    print("------------------")

    pending = sum(1 for todo in todos if not todo["done"])
    print(f"Pending: {pending} | Done: {len(todos) - pending}")


def mark_done(todos: list, todo_id: int) -> None:
    for todo in todos:
        if todo["id"] == todo_id:
            todo["done"] = True
            save_todos(todos)
            print(f"Done: {todo['text']}")
            return
    print("No task found with that id.")


def delete_todo(todos: list, todo_id: int) -> None:
    for index, todo in enumerate(todos):
        if todo["id"] == todo_id:
            removed = todos.pop(index)
            save_todos(todos)
            print(f"Deleted: {removed['text']}")
            return
    print("No task found with that id.")


def ask_int(prompt: str):
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("Please enter a number.")
        return None


def main() -> None:
    todos = load_todos()
    print("=" * 40)
    print("TODO LIST")
    print("=" * 40)

    while True:
        print("\n1. Add  2. List  3. Done  4. Delete  5. Clear  0. Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            text = input("What is the task? ").strip()
            if text:
                add_todo(todos, text)
            else:
                print("An empty task cannot be added.")
        elif choice == "2":
            show_todos(todos)
        elif choice == "3":
            show_todos(todos)
            todo_id = ask_int("Id to mark as done: ")
            if todo_id is not None:
                mark_done(todos, todo_id)
        elif choice == "4":
            show_todos(todos)
            todo_id = ask_int("Id to delete: ")
            if todo_id is not None:
                delete_todo(todos, todo_id)
        elif choice == "5":
            confirm = input("Delete everything? (yes/n): ").strip().lower()
            if confirm == "yes":
                todos.clear()
                save_todos(todos)
                print("All clear.")
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Please choose 1-5 or 0.")


if __name__ == "__main__":
    main()
