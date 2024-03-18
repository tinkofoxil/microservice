import pytest
from uuid import uuid4
from pydantic import ValidationError
from app.models.delivery import Delivery, DeliveryStatuses


@pytest.fixture()
def any_delivery() -> Delivery:
    return Delivery(
        id=uuid4(),
        title='Test Delivery',
        description='Delivery description',
        status=DeliveryStatuses.ACTIVATE,
        user_id=uuid4()
    )


def test_delivery_creation(any_delivery: Delivery):
    assert dict(any_delivery) == {
        'id': any_delivery.id,
        'title': any_delivery.title,
        'description': any_delivery.description,
        'status': any_delivery.status,
        'user_id': any_delivery.user_id
    }


def test_delivery_invalid_status(any_delivery: Delivery):
    with pytest.raises(ValidationError):
        Delivery(
            id=uuid4(),
            title='Test Delivery',
            description='Delivery description',
            status='invalid_status',
            user_id=uuid4()
        )
