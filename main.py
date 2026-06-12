# main.py
import argparse
from tabulate import tabulate
from utils.storage import load_data, save_data
from models.classes import User, Project, Task

def main():
    # Load data right at launch
    users = load_data()

    parser = argparse.ArgumentParser(description="Developer Project Tracker CLI Workstation")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 1. Command: add-user
    cmd_user = subparsers.add_parser("add-user", help="Create a user profile")
    cmd_user.add_argument("--name", required=True, help="User's name")
    cmd_user.add_argument("--email", required=True, help="User's email address")

    # 2.  add-project
    cmd_proj = subparsers.add_parser("add-project", help="Assign a project to a user ID")
    cmd_proj.add_argument("--user-id", type=int, required=True, help="ID of the owner user")
    cmd_proj.add_argument("--title", required=True, help="Project title")
    cmd_proj.add_argument("--desc", required=True, help="Project description details")
    cmd_proj.add_argument("--due", required=True, help="Project due date")

    # 3. add-task
    cmd_task = subparsers.add_parser("add-task", help="Append an action item to a project ID")
    cmd_task.add_argument("--project-id", type=int, required=True, help="ID of the target project")
    cmd_task.add_argument("--title", required=True, help="Task title")
    cmd_task.add_argument("--assign", required=True, help="Name of person assigned")

    # 4.  complete-task
    cmd_comp = subparsers.add_parser("complete-task", help="Set a task status to Completed")
    cmd_comp.add_argument("--task-id", type=int, required=True, help="ID of target task item")

    # 5.  list
    subparsers.add_parser("list", help="Display all structural logs")

    args = parser.parse_args()

   #Routing for top-level commands with basic error handling and success messages

    if args.command == "add-user":
        new_user = User(args.name, args.email)
        users.append(new_user)
        save_data(users)
        print(f"Success: Registered User '{new_user.name}' with ID {new_user.user_id}")

    elif args.command == "add-project":
        found_user = None
        for u in users:
            if u.user_id == args.user_id:
                found_user = u
                break
        
        if found_user is not None:
            new_project = Project(args.title, args.desc, args.due)
            found_user.projects.append(new_project)
            save_data(users)
            print(f"Success: Linked Project '{new_project.title}' (ID {new_project.project_id}) to user {found_user.name}")
        else:
            print(f"Error: User ID {args.user_id} does not exist.")

    elif args.command == "add-task":
        found_project = None
        for u in users:
            for p in u.projects:
                if p.project_id == args.project_id:
                    found_project = p
                    break
        
        if found_project is not None:
            new_task = Task(args.title, args.assign)
            found_project.tasks.append(new_task)
            save_data(users)
            print(f"Success: Appended Task '{new_task.title}' (ID {new_task.task_id}) to Project '{found_project.title}'")
        else:
            print(f"Error: Project ID {args.project_id} not found.")

    elif args.command == "complete-task":
        task_found = False
        for u in users:
            for p in u.projects:
                for t in p.tasks:
                    if t.task_id == args.task_id:
                        t.status = "Completed"  # Fires our encapsulation validation c
                        task_found = True
                        break
        
        if task_found == True:
            save_data(users)
            print(f"Success: Task item {args.task_id} marked as Completed.")
        else:
            print(f"Error: Task ID {args.task_id} could not be found.")

    elif args.command == "list":
        rows = []
        for u in users:
            for p in u.projects:
                for t in p.tasks:
                    rows.append([u.name, u.email, p.title, p.due_date, t.title, t.assigned_to, t.status, t.task_id])
                    
        if len(rows) == 0:
            print("The project system database is completely empty.")
        else:
            headers = ["User", "Email", "Project Title", "Due Date", "Task Title", "Assigned Contributor", "Status", "Task ID"]
            print(tabulate(rows, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    main()