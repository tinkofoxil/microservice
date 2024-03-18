import traceback
import uuid
from uuid import UUID

import requests

from app.models.telivery import Delivery, DeliveryStatuses
from app.repositories.bd_telivery_repo import DeliveryRepo
from app.rabbitmq_produce import send_notification


class DeliveryService:
    telivery_repo: DeliveryRepo

    def __init__(self) -> None:
        self.telivery_repo = DeliveryRepo()

    def get_teliverys(self) -> list[Delivery]:
        return self.telivery_repo.get_teliverys()

    def create_telivery(self, title: str, description: str, user_id: UUID):
        new_telivery = Delivery(id=uuid.uuid4(), title=title, description=description, user_id=user_id,
                            status=DeliveryStatuses.ACTIVATE)
        send_notification(new_telivery)
        return self.telivery_repo.create_telivery(new_telivery)

    def done_telivery(self, telivery_id: UUID) -> Delivery:
        telivery = self.telivery_repo.get_telivery_by_id(telivery_id)

        if telivery.status == DeliveryStatuses.DONE:
            raise ValueError

        telivery.status = DeliveryStatuses.DONE
        send_notification(telivery)
        return self.telivery_repo.done_telivery(telivery)
