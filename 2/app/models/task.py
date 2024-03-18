import enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TaskStatuses(enum.Enum):
    ACTIVATE = 'activate'
    DONE = 'done'


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    description: str
    status: TaskStatuses
    user_id: UUID
