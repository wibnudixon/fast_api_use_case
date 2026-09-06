from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from app.api.dependencies import get_task_service
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.tasks import TaskService

router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    payload: TaskCreate,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """Create a task."""
    return service.create_task(payload)


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    service: TaskService = Depends(get_task_service),
) -> list[TaskResponse]:
    """List every task."""
    return service.list_tasks()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: UUID,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """Return one task."""
    return service.get_task(task_id)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: UUID,
    payload: TaskUpdate,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """Partially update one task."""
    return service.update_task(task_id, payload)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: UUID,
    service: TaskService = Depends(get_task_service),
) -> Response:
    """Delete one task."""
    service.delete_task(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)