import json
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

TASKS_FILE = Path("tracker.json")


# ---------- Load / Save ----------

def load_tasks():
    if TASKS_FILE.exists():
        with open(TASKS_FILE, "r") as f:
            data = json.load(f)
            # Support old flat-list format
            if isinstance(data, list):
                return {"todo": data, "done": []}
            return data
    return {"todo": [], "done": []}


def save_tasks(data):
    with open(TASKS_FILE, "w") as f:
        json.dump(data, f, indent=4)


def time_now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ---------- Commands ----------

def add_task():
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    due_date = input("Enter due date (YYYY-MM-DD): ").strip()
    due_time = input("Enter due time (HH:MM): ").strip()

    task = {
        "title": title,
        "description": description,
        "due_date": due_date,
        "due_time": due_time,
    }

    data = load_tasks()
    data["todo"].append(task)
    save_tasks(data)
    print("Task added successfully!")


def update_task():
    data = load_tasks()
    if not data["todo"]:
        print("No tasks to update.")
        return

    print_list(data["todo"])
    task_num = int(input("Enter the ID of the task to update: "))
    if 1 <= task_num <= len(data["todo"]):
        task = data["todo"][task_num - 1]
        print("Leave fields blank to keep current values.")
        task["title"]       = input(f"Title (current: {task['title']}): ")                    or task["title"]
        task["description"] = input(f"Description (current: {task['description']}): ")        or task["description"]
        task["due_date"]    = input(f"Due date (current: {task['due_date']}): ").strip()       or task["due_date"]
        task["due_time"]    = input(f"Due time (current: {task['due_time']}): ").strip()       or task["due_time"]
        save_tasks(data)
        print("Task updated successfully!")
    else:
        print("Invalid task number.")


def delete_task():
    data = load_tasks()
    if not data["todo"]:
        print("No tasks to delete.")
        return

    print_list(data["todo"])
    task_num = int(input("Enter the number of the task to delete: "))
    if 1 <= task_num <= len(data["todo"]):
        del data["todo"][task_num - 1]
        save_tasks(data)
        print("Task deleted successfully!")
    else:
        print("Invalid task number.")


def delete_all_tasks():
    confirm = input("Are you sure you want to delete all tasks? (yes/no): ")
    if confirm.lower() == "yes":
        save_tasks({"todo": [], "done": []})
        print("All tasks deleted successfully!")
    elif confirm.lower() == "no":
        print("Operation cancelled.")
    else:
        print("Invalid input, operation cancelled.")


def mark_task_completed():
    data = load_tasks()
    if not data["todo"]:
        print("No tasks to mark as completed.")
        return

    print_list(data["todo"])
    task_num = int(input("Enter the ID of the task to mark as completed: "))
    if 1 <= task_num <= len(data["todo"]):
        task = data["todo"].pop(task_num - 1)
        task["completed_at"] = time_now()
        data["done"].append(task)
        save_tasks(data)
        print(f"Task '{task['title']}' moved to Done!")
    else:
        print("Invalid task number.")


def list_tasks():
    data = load_tasks()

    print("\n===== TO-DO =====")
    if data["todo"]:
        print_list(data["todo"])
    else:
        print("  No pending tasks.")

    print("\n===== DONE =====")
    if data["done"]:
        print_list(data["done"])
    else:
        print("  No completed tasks yet.")
    print()


# ---------- Helper ----------

def print_list(tasks):
    for idx, task in enumerate(tasks, start=1):
        due_date = task.get("due_date", "N/A")
        due_time = task.get("due_time", "N/A")
        completed_at = task.get("completed_at", "")
        if completed_at:
            print(f"  {idx}. {task['title']} - Completed: {completed_at}")
        else:
            print(f"  {idx}. {task['title']} - Due: {due_date} at {due_time}")
        print(f"     Description: {task['description']}")


# ---------- Main ----------

def main():
    parser = ArgumentParser(description="Simple task tracker")
    parser.add_argument("command", choices=[
        "add.task", "list.tasks", "update.task",
        "delete.task", "delete.all.tasks", "mark.completed"
    ], help="Command to execute")
    args = parser.parse_args()

    if args.command == "add":
        add_task()
    elif args.command == "list":
        list_tasks()
    elif args.command == "update":
        update_task()
    elif args.command == "delete":
        delete_task()
    elif args.command == "delete.all":
        delete_all_tasks()
    elif args.command == "mark.done":
        mark_task_completed()
    else:
        print("Unknown command! Try something else.")


if __name__ == "__main__":
    main()