# CLI Task Manager (Python+Git)

A simple, fast, and structured **Command Line Task Manager** built with Python.
This project demonstrates clean architecture, object-oriented design, persistence, and CLI tooling.

---

## Features

Create tasks
Update tasks
Delete tasks
Mark tasks as completed
Filter tasks by status
Sort tasks by priority or created_at
View a single task
List all tasks
Persistent storage using JSON
Clean CLI powered by `argparse`

---

## Project Architecture

```
task_manager_cli/
│
├── models/        → Domain models (Task, Enums)
├── services/      → Business logic (TaskManager)
├── storage/       → Persistence layer (JSON storage)
├── data/          → Stored tasks
├── task_cli.py    → CLI entry point
```

**Design Principle Used:**

Separation of Concerns
Encapsulation
Lifecycle-aware models
Service-based architecture

---

## Installation

### 1. Clone the repository

```
git clone <your-repo-url>
cd task_manager_cli
```

### 2. Create virtual environment

```
python -m venv .venv
```

### 3. Activate it

**Windows**

```
.venv\Scripts\activate
```

**Mac/Linux**

```
source .venv/bin/activate
```

---

## How to Run

```
python task_cli.py --help
```

---

## CLI Usage

###  Add Task

```
python task_cli.py add --title "Build CLI tool" --description "Using argparse" --priority high
```

---

###  List Tasks

```
python task_cli.py list
```

---

###  Get One Task

```
python task_cli.py get <task_id>
```

---

###  Complete Task

```
python task_cli.py complete <task_id>
```

---

###  Update Task

```
python task_cli.py update <task_id> --title "New Title" --description "New description" --priority low
```
```
python task_cli.py update <task_id> --title "New Title only"
```
```
python task_cli.py update <task_id> --description "New description only" 
```
```
python task_cli.py update <task_id> --priority medium
```

---

###  Delete Task

```
python task_cli.py delete <task_id>
```

---

###  Filter by Status

```
python task_cli.py status_filter pending
```


---

###  Sort by Priority or created_at

```
python task_cli.py sort priority
```

```
python task_cli.py sort created_at
```

---

##  What This Project Demonstrates

This is **not just a CRUD app.**

It showcases understanding of:

* Object-Oriented Programming
* Data Modeling
* Enum usage
* Private vs public attributes
* Persistence
* CLI design
* Error handling
* Clean code structure

---

##  Future Improvements

* Search tasks
* Due dates
* Unit tests
* Colored terminal output
* SQLite storage
* Packaging as an installable CLI

---

##  Author

Built as a demo project to strengthen backend engineering fundamentals and CLI design skills.
