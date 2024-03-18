# /app/repositories/bd_delivery_repo.py

import traceback
from uuid import UUID
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.delivery import Delivery
from app.schemas.delivery import Delivery as DBDelivery


class DeliveryRepo:
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, delivery: DBDelivery) -> Delivery:
        result = dict(Delivery.model_validate(delivery))
        result = Delivery(id=result["id"], title=result["title"], description=result["description"], status=result["status"], user_id=result["user_id"])
        return result

    def _map_to_schema(self, delivery: Delivery) -> DBDelivery:
        data = dict(delivery)
        # del data['delivery']
        data['id'] = delivery.id if delivery != None else None
        result = DBDelivery(**data)

        return result

    def get_deliverys(self) -> list[Delivery]:
        deliverys = []
        for t in self.db.query(DBDelivery).all():
            deliverys.append(t)
        return deliverys

    def get_delivery_by_id(self, id: UUID) -> Delivery:
        delivery = self.db \
            .query(DBDelivery) \
            .filter(DBDelivery.id == id) \
            .first()
        delivery = self._map_to_model(delivery)
        if delivery == None:
            raise KeyError
        return delivery

    def create_delivery(self, delivery: Delivery) -> Delivery:
        try:
            db_delivery = self._map_to_schema(delivery)
            self.db.add(db_delivery)
            self.db.commit()
            return delivery
        except:
            traceback.print_exc()
            raise KeyError

    def done_delivery(self, delivery: Delivery) -> Delivery:
        db_delivery = self.db.query(DBDelivery).filter(
            DBDelivery.id == delivery.id).first()
        db_delivery.status = delivery.status
        self.db.commit()
        return self._map_to_model(db_delivery)
