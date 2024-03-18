from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.models.delivery import Delivery
from app.services.delivery_service import DeliveryService

delivery_router = APIRouter(prefix='/delivery', tags=['Delivery'])


@delivery_router.get('/')
def get_deliverys(delivery_service: DeliveryService = Depends(DeliveryService)) -> list[Delivery]:
    return delivery_service.get_deliverys()


@delivery_router.post('/{id}/done')
def done_delivery(id: UUID, delivery_service: DeliveryService = Depends(DeliveryService)) -> Delivery:
    try:
        delivery = delivery_service.done_delivery(id)
        return delivery
    except KeyError:
        raise HTTPException(404, f'Delivery with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Delivery with id={id} can\'t be done')
