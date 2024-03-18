from typing import List
from uuid import UUID

from app.models.delivery import Delivery, DeliveryStatuses

deliverys: List[Delivery] = []


class DeliveryRepo:
    def get_deliverys(self) -> list[Delivery]:
        return deliverys

    def get_delivery_by_id(self, delivery_id: UUID) -> Delivery:
        for t in deliverys:
            if t.id == delivery_id:
                return t

        raise KeyError

    def create_delivery(self, new_delivery: Delivery) -> Delivery:
        if len([t for t in deliverys if t.id == new_delivery.id]) > 0:
            raise KeyError

        deliverys.append(new_delivery)

        return new_delivery

    def done_delivery(self, delivery: Delivery) -> Delivery:
        for t in deliverys:
            if t.id == delivery.id:
                t.status = delivery.status
                break

        return delivery
