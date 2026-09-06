from datetime import UTC, datetime
from uuid import UUID, uuid4
from app.core.errors import ResourceNotFoundError
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate


class TaskService:
    """Manage tasks using temporary in-memory storage."""

    def __init__(self) -> None:
        self._tasks: dict[UUID, TaskResponse] = {}

    def create_task(self, payload: TaskCreate) -> TaskResponse:
        """Create and store a task."""
        now = datetime.now(UTC)

        task = TaskResponse(
            id=uuid4(),
            title=payload.title,
            description=payload.description,
            status=payload.status,
            priority=payload.priority,
            due_date=payload.due_date,
            created_at=now,
            updated_at=now,
        )

        self._tasks[task.id] = task
        return task

    def list_tasks(self) -> list[TaskResponse]:
        """Return all stored tasks."""
        return list(self._tasks.values())

    def get_task(self, task_id: UUID) -> TaskResponse:
        """Return one task or raise a domain-specific error."""
        task = self._tasks.get(task_id)

        if task is None:
            raise ResourceNotFoundError("TaskNotFoundError")

        return task

    def update_task(self, task_id: UUID, payload: TaskUpdate) -> TaskResponse:
        """Partially update one task."""
        task = self.get_task(task_id)
        updates = payload.model_dump(exclude_unset=True)

        updated_task = task.model_copy(
            update={
                **updates,
                "updated_at": datetime.now(UTC),
            }
        )

        self._tasks[task_id] = updated_task
        return updated_task

    def delete_task(self, task_id: UUID) -> None:
        """Delete one task."""
        self.get_task(task_id)
        del self._tasks[task_id]


    def clear_tasks(self) -> None:
        """Clear all tasks; used to isolate local tests."""
        self._tasks.clear()



# A few improvements are worth considering:

# 1- Avoid exposing mutable stored models. 
# create_task, get_task, and list_tasks return the same TaskResponse objects held in _tasks (tasks.py:29, tasks.py:35). Any non-HTTP caller could mutate a returned task and silently change storage without updating updated_at. Make TaskResponse immutable (ConfigDict(frozen=True)) or return model_copy() values at service boundaries.

# 2- Define empty PATCH behavior. TaskUpdate allows {}, and update_task will then only change updated_at (tasks.py:44). That can be acceptable, but APIs often reject an empty partial update with 422, usually via a schema validator. Decide and test the intended contract.

# 3- Raise an exception instance with context. raise TaskNotFoundError works in Python, but raise TaskNotFoundError(f"Task {task_id} was not found") (tasks.py:39) is clearer for logs, reuse outside this router, and debugging.
# 4- Concurrency is intentionally unsupported. The singleton service is shared by the app, while a read-modify-write update is not atomic (tasks.py:44). Fine for temporary learning storage, as the docstring says; move to a database/repository or add synchronization before treating it as production storage.
# 5- Minor cleanup: remove the extra blank lines before clear_tasks (tasks.py:63). The test-only clear_tasks method itself is practical given the shared dependency.