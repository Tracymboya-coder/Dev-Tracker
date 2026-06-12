# DevTrack CLI - Multi-User Project Tracker

DevTrack CLI is a simple, terminal-based project management tool designed for software development teams. It allows you to create user profiles for developers, assign projects to those users, and break those projects down into actionable tasks with custom assignments and status tracking. 

To ensure that your work is saved, the application automatically loads and saves all records using a local JSON file database.

---

## 🛠️ Project Structure
The project is built using a clean, modular folder layout:

* **`main.py`**: The main entry point of the app that reads terminal commands.
* **`models/classes.py`**: Contains the core blueprints (Person, User, Project, Task).
* **`utils/storage.py`**: Handles loading data from and saving data to the hard drive.
* **`data/tracker_data.json`**: The text database file where all project logs live.
* **`requirements.txt`**: Lists external software packages needed (`tabulate`).

---

## ⚙️ Requirements & Installation

This project requires **Python 3.10+** and the external **`tabulate`** package for displaying clean tables.

### 1. Set Up Your Virtual Environment (Sandbox)
Open your terminal inside the project folder and run:

* **On Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
🚀 How to Use (CLI Commands)
Always ensure your virtual environment is active (venv) before running commands. The tool automatically counts and generates unique IDs for users, projects, and tasks.

1. Add a New User
Registers a developer profile in the system.

Bash
python main.py add-user --name "Alice Smith" --email "alice@code.com"
2. Add a Project
Links a new project milestone to an existing user using their generated User ID.

Bash
python main.py add-project --user-id 1 --title "Web Portfolio" --desc "Build frontend layouts" --due "2026-06-30"
3. Add a Task
Appends a specific task to a project using its generated Project ID.

Bash
python main.py add-task --project-id 1 --title "Fix CSS Grid margins" --assign "Alice Smith"
4. Complete a Task
Changes a task's status from "Pending" to "Completed" using its Task ID.

Bash
python main.py complete-task --task-id 1
5. View Dashboard (List Everything)
Generates a clean spreadsheet-style grid table of all active users, projects, and tasks.

Bash
python main.py list
6. Delete Commands
Removes items completely from the local database:

Bash
# Delete a user profile completely
python main.py delete-user --user-id 1

# Delete a specific project
python main.py delete-project --project-id 1

# Delete a single task
python main.py delete-task --task-id 1
💡 Technical Features Covered
This project directly satisfies all standard academic object-oriented design and interface guidelines:

Inheritance: The User class inherits shared traits from a base Person class.

Encapsulation: Protects variables (like _status) and utilizes Python @property getters/setters to validate state shifts.

Persistence: Handles full local File I/O manipulation via native JSON parsing protocols wrapped in defensive try/except error-handling checkpoints.