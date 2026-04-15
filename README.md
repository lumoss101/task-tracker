# Taskly - Command Line Task Tracker

A simple command-line task tracker built in Python. Tasks are stored locally in a JSON file and organized into two lists: **To-Do** and **Done**.

# This project was a part of a Roadmap Sh Challange that you can access in https://roadmap.sh/projects/task-tracker

---

## Requirements

- Python 3.x

No external libraries needed.

---

## Setup

1. Clone or download the repository:
   ```
   git clone https://github.com/lumoss101/task-tracker
   cd task-tracker
   ```

2. Run the script directly with Python:
   ```
   python taskly.py <command>
   ```

---

## Commands

| Command | Description |
|---|---|
| `add` | Add a new task (prompts for details) |
| `list` | List all tasks (To-Do and Done) |
| `update` | Update an existing task |
| `delete` | Delete a task from the To-Do list |
| `delete.all` | Delete all tasks (requires confirmation) |
| `mark.done` | Move a task from To-Do to Done |

---

## Usage Examples

```bash
# Add a task
python taskly.py add

# List all tasks
python taskly.py list

# Update a task
python taskly.py update

# Mark a task as completed
python taskly.py mark.done

# Delete a task
python taskly.py delete

# Delete all tasks
python taskly.py delete.all
```

---

## How It Works

- Tasks are saved in a `mytasktracker.json` file created automatically in the same folder as the script.
- When you run `add`, you will be prompted to enter the title, description, due date, and due time.
- When you run `mark.done`, the task is moved from the **To-Do** list to the **Done** list and stamped with a completion time.
- Running `list` displays both lists separately.

---

## Data Format

Tasks are stored in `mytasktracker.json` in the following format:

```json
{
    "todo": [
        {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "due_date": "2026-04-16",
            "due_time": "10:00"
        }
    ],
    "done": [
        {
            "title": "Write report",
            "description": "Q1 summary report",
            "due_date": "2026-04-10",
            "due_time": "09:00",
            "completed_at": "2026-04-10 08:45:00"
        }
    ]
}
```
