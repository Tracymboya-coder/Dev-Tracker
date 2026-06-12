

class Person:
    """Base class ."""
    def __init__(self, name):
        self._name = name  

    @property
    def name(self):
        return self._name


class User(Person):
    """User inherits from Person."""
    id_counter = 1 

    def __init__(self, name, email):
        
        super().__init__(name)
        self.user_id = User.id_counter
        User.id_counter += 1
        
        self.email = email
        self.projects = []  # One-to-Many relationship (User -> Projects)

    def __str__(self):
        return f"User: {self.name} (ID: {self.user_id})"


class Project:
    id_counter = 1

    def __init__(self, title, description, due_date):
        self.project_id = Project.id_counter
        Project.id_counter += 1
        
        self.title = title
        self.description = description
        self.due_date = due_date
        self.tasks = []  # One-to-Many relationship (Project -> Tasks)

    def __str__(self):
        return f"Project: {self.title} (ID: {self.project_id})"


class Task:
    id_counter = 1

    def __init__(self, title, assigned_to):
        self.task_id = Task.id_counter
        Task.id_counter += 1
        
        self.title = title
        self.assigned_to = assigned_to
        self._status = "Pending"  

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        """Property setter to satisfy the encapsulation requirement."""
        if new_status == "Pending" or new_status == "Completed":
            self._status = new_status
        else:
            print("Error: Status must be Pending or Completed")

    def __str__(self):
        return f"Task: {self.title} (Status: {self._status})"