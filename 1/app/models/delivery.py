import enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DeliveryStatuses(enum.Enum):
    ACTIVATE = 'activate'
    DONE = 'done'


class Delivery(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    description: str
    status: DeliveryStatuses
    user_id: UUID
