import json
import os
import sys

DATA_FILE = "todo_list.json"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("⚠️ Warning: Data file was corrupted. Starting with an empty list.")
        return []

def save_tasks(tasks):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=4)
    except IOError:
        print("❌ Error: Could not save tasks to file.")

def add_task(tasks):
    title = input("\nEnter the task description: ").strip()
    if title:
        tasks.append({"title": title, "completed": False})
        save_tasks(tasks)
        print(f"✅ Task '{title}' added successfully!")
    else:
        print("❌ Task description cannot be empty.")

def view_tasks(tasks):
    if not tasks:
        print("\n📝 Your To-Do list is empty!")
        return

    print("\n--- Your To-Do List ---")
    for index, task in enumerate(tasks, start=1):
        status = "🟢 [Done]" if task["completed"] else "🔴 [Pending]"
        print(f"{index}. {status} {task['title']}")
    print("-" * 23)

def mark_completed(tasks):
    view_tasks(tasks)
    if not tasks:
        return

    try:
        choice = int(input("\nEnter the number of the task to mark complete: "))
        if 1 <= choice <= len(tasks):
            tasks[choice - 1]["completed"] = True
            save_tasks(tasks)
            print(f"Task marked as completed!")
        else:
            print("❌ Invalid task number.")
    except ValueError:
        print("❌ Please enter a valid number.")

def remove_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    
    try:
        choice = int(input("\nEnter the number of the task to remove: "))
        if 1 <= choice <= len(tasks):
            removed = tasks.pop(choice - 1)
            save_tasks(tasks)
            print(f"🗑️ Removed task: '{removed['title']}'")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")
        
def main():
    tasks = load_tasks()

    while True:
        print("\n|| To-Do CLI Application ||")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Mark Task Completed")
        print("4. Remove Task")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            view_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            mark_completed(tasks)
        elif choice == "4":
            remove_task(tasks)
        elif choice == "5":
            print("\nGoodbye! Have a productive day!")
            sys.exit()
        else:
            print("❌ Invalid choice. Please select a number between 1 and 5.")

main()