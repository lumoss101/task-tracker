import json
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

TASKS_FILE = Path("tracker.json")

def add_task():
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    due_date_str = input("Enter due date (YYYY-MM-DD): ")
    due_time_str = input("Enter due time (HH:MM): ")
    due_date = due_date_str.strip()
    due_time = due_time_str.strip()

    task = {
        "title": title,
        "description": description,
        "due_date": due_date,
        "due_time": due_time,
    }

    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    print("Task added successfully!")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found")
        return

    for idx, task in enumerate(tasks, start=1):
        due_time = task.get('due_time', 'N/A')
        due_date = task.get('due_date', 'N/A')
        print(f"{idx}. {task['title']} - Due: {due_date} at {due_time}")
        print(f"   Description: {task['description']}")

def load_tasks():
    if TASKS_FILE.exists():
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def delete_task():
    tasks = load_tasks()
    if not tasks:
        print("No tasks to delete")
        return

    list_tasks()
    task_num = int(input("Enter the number of the task to delete: "))
    if 1 <= task_num <= len(tasks):
        del tasks[task_num - 1]
        save_tasks(tasks)
        print("Task deleted successfully!")
    else:
        print("Invalid task number")

def delete_all_tasks():
    confirm = input("Are you sure you want to delete all tasks? (yes/no): ")
    if confirm.lower() == "yes":
        save_tasks([])
        print("All tasks deleted successfully!")
    elif confirm.lower() == "no":
        print("Operation cancelled")
    else:
        print("Invalid input, operation cancelled")

def main():
    parser = ArgumentParser(description="Simple task tracker")
    parser.add_argument("command", choices=["add.task", "list.of.tasks", "delete.task", "delete.all.tasks"], help="Command to execute")
    args = parser.parse_args()

    if args.command == "add.task":
        add_task()
    elif args.command == "list.of.tasks":
        list_tasks()
    elif args.command == "delete.task":
        delete_task()
    elif args.command == "delete.all.tasks":
        delete_all_tasks()
    else:
        print("Unknown command")
        
if __name__ == "__main__":
    main()