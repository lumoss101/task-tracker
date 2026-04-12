import json
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

TASKS_FILE = Path("tasks.json")


# ---------- File helpers ----------

def load_tasks() -> list:
    if not TASKS_FILE.exists():
        return []
    with TASKS_FILE.open() as f:
        return json.load(f)


def save_tasks(tasks: list) -> None:
    with TASKS_FILE.open("w") as f:
        json.dump(tasks, f, indent=2)


def next_id(tasks: list) -> int:
    return max((t["id"] for t in tasks), default=0) + 1


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ---------- Core actions ----------

def add_task(description: str) -> None:
    tasks = load_tasks()
    task = {
        "id": next_id(tasks),
        "description": description,
        "status": "todo",
        "createdAt": now(),
        "updatedAt": now(),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added (ID: {task['id']})")


def update_task(task_id: int, description: str) -> None:
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = description
            task["updatedAt"] = now()
            save_tasks(tasks)
            print(f"Task {task_id} updated.")
            return
    print(f"Task {task_id} not found.")


def delete_task(task_id: int) -> None:
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        print(f"Task {task_id} not found.")
        return
    save_tasks(new_tasks)
    print(f"Task {task_id} deleted.")


def mark_task(task_id: int, status: str) -> None:
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = now()
            save_tasks(tasks)
            print(f"Task {task_id} marked as '{status}'.")
            return
    print(f"Task {task_id} not found.")


def list_tasks(filter_status: str = None) -> None:
    tasks = load_tasks()
    if filter_status:
        tasks = [t for t in tasks if t["status"] == filter_status]
    if not tasks:
        print("No tasks found.")
        return
    status_icons = {"todo": "○", "in-progress": "◑", "done": "●"}
    for t in tasks:
        icon = status_icons.get(t["status"], "?")
        print(f"[{t['id']}] {icon} {t['description']}  ({t['status']})  — {t['updatedAt']}")


# ---------- CLI setup ----------

def build_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="task",
        description="A simple command-line task tracker."
    )
    sub = parser.add_subparsers(dest="command", metavar="command")
    sub.required = True

    # add
    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("description", help="Task description")

    # update
    p_update = sub.add_parser("update", help="Update a task's description")
    p_update.add_argument("id", type=int, help="Task ID")
    p_update.add_argument("description", help="New description")

    # delete
    p_delete = sub.add_parser("delete", help="Delete a task")
    p_delete.add_argument("id", type=int, help="Task ID")

    # mark-in-progress
    p_mip = sub.add_parser("mark-in-progress", help="Mark a task as in progress")
    p_mip.add_argument("id", type=int, help="Task ID")

    # mark-done
    p_done = sub.add_parser("mark-done", help="Mark a task as done")
    p_done.add_argument("id", type=int, help="Task ID")

    # list
    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument(
        "filter",
        nargs="?",
        choices=["done", "todo", "in-progress"],
        default=None,
        help="Filter by status (done | todo | in-progress)"
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "update":
        update_task(args.id, args.description)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "mark-in-progress":
        mark_task(args.id, "in-progress")
    elif args.command == "mark-done":
        mark_task(args.id, "done")
    elif args.command == "list":
        list_tasks(args.filter)


if __name__ == "__main__":
    main()