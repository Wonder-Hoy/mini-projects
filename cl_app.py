import json
import os
import sys
from google import genai
from google.genai import errors

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

def ask_ai_assistant(tasks):
    print("\nXander: Wassup dahg?")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: Xander does not have a KEY and is slacking off!")
        return

    client = genai.Client()
    
    task_list_str = "\n".join([f"- {t['title']} (Completed: {t['completed']})" for t in tasks])
    if not task_list_str:
        task_list_str = "Why you lazy nyan~."

    print("Type 'exit' to return to the main menu.")
    
    try:
        # AI prompt
        chat = client.chats.create(
            model="gemini-3.5-flash",
            config={
                "system_instruction": f"You are a helpful productivity assistant. The user's current to-do list is:\n{task_list_str}\nHelp them prioritize, break down tasks, or give advice."
            }
        )
        
        while True:
            user_input = input("\nYou: ")
            
            if user_input.lower() in ['exit', 'quit', 'back']:
                print("Returning to main menu...")
                break
                
            if not user_input.strip():
                continue

            try:
                print("Xander: ", end="", flush=True)
                response = chat.send_message_stream(user_input)
                for chunk in response:
                    print(chunk.text, end="", flush=True)
                print("\n")
                
            except errors.APIError as e:
                print(f"\nAPI Error: {e}")
                
    except Exception as e:
        print(f"\nAn error occurred: {e}")

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
        print("5. Ask AI Assistant")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            view_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            mark_completed(tasks)
        elif choice == "4":
            remove_task(tasks)
        elif choice == "5":
            ask_ai_assistant(tasks)
        elif choice == "6":
            print("\nGoodbye! Have a productive day!")
            sys.exit()
        else:
            print("❌ Invalid choice. Please select a number between 1 and 6.")

main()