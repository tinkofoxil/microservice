import traceback
import uuid
from uuid import UUID

import requests

from app.models.delivery import Delivery, DeliveryStatuses
from app.repositories.bd_delivery_repo import DeliveryRepo
from app.rabbitmq_produce import send_notification


class DeliveryService:
    delivery_repo: DeliveryRepo

    def __init__(self) -> None:
        self.delivery_repo = DeliveryRepo()

    def get_deliverys(self) -> list[Delivery]:
        return self.delivery_repo.get_deliverys()

    def create_delivery(self, title: str, description: str, user_id: UUID):
        new_delivery = Delivery(id=uuid.uuid4(), title=title, description=description, user_id=user_id,
                            status=DeliveryStatuses.ACTIVATE)
        send_notification(new_delivery)
        return self.delivery_repo.create_delivery(new_delivery)

    def done_delivery(self, delivery_id: UUID) -> Delivery:
        delivery = self.delivery_repo.get_delivery_by_id(delivery_id)

        if delivery.status == DeliveryStatuses.DONE:
            raise ValueError

        delivery.status = DeliveryStatuses.DONE
        send_notification(delivery)
        return self.delivery_repo.done_delivery(delivery)
