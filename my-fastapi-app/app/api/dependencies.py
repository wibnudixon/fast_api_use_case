# Importing packages
from app.services.tasks import TaskService
# Creating a single instance of the TaskService to be shared across the application
task_service = TaskService()


def get_task_service() -> TaskService:
    """Provide the shared task service for request handlers."""
    return task_service