import os
import pytest

# Import our system blueprints and storage engines
from models.classes import User, Project, Task
from utils.storage import save_data, load_data

# --- 1. THE SETTING FIXTURE (The Sandbox Sandbox) ---

@pytest.fixture
def test_env():
    """Sets up a clean test database before a test runs, and deletes it after."""
    test_filename = "data/test_database.json"
    sample_users = []
    
    # Create baseline sample user
    user = User("Test Dev", "test@dev.com")
    user.user_id = 1
    sample_users.append(user)
    
    # Hand this data over to the test functions
    yield test_filename, sample_users, user
    
    # Tear Down: Wipe the sandbox file out after the test finishes
    if os.path.exists(test_filename):
        os.remove(test_filename)


# --- 2. THE TEST CASES ---

def test_user_creation():
    """Test if User object properties are correctly initialized."""
    new_user = User("Bob Builder", "bob@build.com")
    
    assert new_user.name == "Bob Builder"
    assert new_user.email == "bob@build.com"
    assert new_user.projects == []


def test_task_status_setter_validation():
    """Test if the @property setter safely guards the task status."""
    task = Task("Write Unit Tests", "Test Dev")
    
    # Should default to Pending
    assert task.status == "Pending"
    
    # Valid state change should work
    task.status = "Completed"
    assert task.status == "Completed"
    
    # Invalid state change should be blocked (remains unchanged)
    task.status = "Banana"
    assert task.status == "Completed"


def test_save_and_load_pipeline(test_env):
    """Test if storage.py completely preserves data structures through serialization."""
    # Unpack our setup environment data from the fixture
    test_filename, sample_users, user = test_env
    
    # Add a mock project and task to our sample user
    project = Project("App UX", "Design Figma layouts", "2026-07-01")
    project.project_id = 1
    
    task = Task("Draw Wireframes", "Test Dev")
    task.task_id = 1
    
    project.tasks.append(task)
    user.projects.append(project)

    # 1. Trigger the Save Engine
    save_data(sample_users, filename=test_filename)
    assert os.path.exists(test_filename)

    # 2. Trigger the Load Engine
    reloaded_users = load_data(filename=test_filename)

    # 3. Verify everything matches perfectly
    assert len(reloaded_users) == 1
    assert reloaded_users[0].name == "Test Dev"
    assert reloaded_users[0].projects[0].title == "App UX"
    assert reloaded_users[0].projects[0].tasks[0].title == "Draw Wireframes"
    assert reloaded_users[0].projects[0].tasks[0].status == "Pending"