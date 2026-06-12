
import json
import os
from models.classes import User, Project, Task

DATA_FILE = "data/tracker_data.json"

def save_data(users_list):
    """Saves data by building basic dictionaries with standard loops."""
    all_data = []

    for user in users_list:
        user_dict = {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "projects": []
        }
        
        for project in user.projects:
            project_dict = {
                "project_id": project.project_id,
                "title": project.title,
                "description": project.description,
                "due_date": project.due_date,
                "tasks": []
            }
            
            for task in project.tasks:
                task_dict = {
                    "task_id": task.task_id,
                    "title": task.title,
                    "assigned_to": task.assigned_to,
                    "status": task.status
                }
                project_dict["tasks"].append(task_dict)
                
            user_dict["projects"].append(project_dict)
            
        all_data.append(user_dict)

    # Wrap the file writing process in a basic try/except block
    try:
        os.makedirs("data", exist_ok=True)
        with open(DATA_FILE, "w") as file:
            json.dump(all_data, file, indent=4)
    except Exception as e:
        print(f"File writing issue: {e}")


def load_data():
    """Loads data from the JSON file and reconstructs classes."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as file:
            all_data = json.load(file)
            
        loaded_users = []
        
        for u_data in all_data:
            user = User(u_data["name"], u_data["email"])
            user.user_id = u_data["user_id"]  # Restore old ID
            
            for p_data in u_data["projects"]:
                project = Project(p_data["title"], p_data["description"], p_data["due_date"])
                project.project_id = p_data["project_id"]  # Restore old ID
                
                for t_data in p_data["tasks"]:
                    task = Task(t_data["title"], t_data["assigned_to"])
                    task.task_id = t_data["task_id"]  # Restore old ID
                    task.status = t_data["status"]
                    
                    project.tasks.append(task)
                user.projects.append(project)
            loaded_users.append(user)
            
        # Adjust counters so new objects get fresh numbers
        if len(loaded_users) > 0:
            max_u = 1
            max_p = 1
            max_t = 1
            for u in loaded_users:
                if u.user_id > max_u: max_u = u.user_id
                for p in u.projects:
                    if p.project_id > max_p: max_p = p.project_id
                    for t in p.tasks:
                        if t.task_id > max_t: max_t = t.task_id
            User.id_counter = max_u + 1
            Project.id_counter = max_p + 1
            Task.id_counter = max_t + 1
            
        return loaded_users

    except Exception:
        print("Data corrupted or empty. Creating a new workspace.")
        return []