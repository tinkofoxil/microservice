from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.delivery import DeliveryStatuses
from app.schemas.base_schema import Base


class Delivery(Base):
    __tablename__ = 'tasks'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[DeliveryStatuses]
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True))
