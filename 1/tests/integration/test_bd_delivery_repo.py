from uuid import uuid4, UUID

import pytest

from app.models.delivery import Delivery, DeliveryStatuses
from app.repositories.bd_delivery_repo import DeliveryRepo


@pytest.fixture()
def delivery_repo() -> DeliveryRepo:
    repo = DeliveryRepo()
    return repo


@pytest.fixture()
def first_delivery() -> Delivery:
    return Delivery(id=UUID("2174e1ed-b7bb-465f-8b43-4867f44dc9f9"), title="Test", description="description",
                status=DeliveryStatuses.ACTIVATE, user_id=UUID("2174e1ed-b7bb-465f-8b43-4867f44dc9f9"))


@pytest.fixture()
def second_delivery() -> Delivery:
    return Delivery(id=uuid4(), title="Test", description="description",
                status=DeliveryStatuses.ACTIVATE, user_id=UUID("2174e1ed-b7bb-465f-8b43-4867f44dc9f9"))


def test_empty_list(delivery_repo: DeliveryRepo) -> None:
    assert delivery_repo.get_deliverys() == []


def test_add_delivery(delivery_repo: DeliveryRepo, first_delivery: Delivery) -> None:
    delivery_repo.create_delivery(first_delivery)
    deliverys = delivery_repo.get_deliverys()
    assert len(deliverys) == 1
    assert deliverys[0].id == first_delivery.id


def test_add_duplicate_delivery_error(delivery_repo: DeliveryRepo, first_delivery: Delivery) -> None:
    with pytest.raises(KeyError):
        delivery_repo.create_delivery(first_delivery)


def test_get_delivery_by_id(delivery_repo: DeliveryRepo, first_delivery: Delivery) -> None:
    retrieved_delivery = delivery_repo.get_delivery_by_id(first_delivery.id)
    assert retrieved_delivery == first_delivery