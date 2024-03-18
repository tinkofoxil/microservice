import pytest
from uuid import uuid4
from app.models.delivery import Delivery, DeliveryStatuses
from app.repositories.local_delivery_repo import DeliveryRepo


@pytest.fixture()
def delivery_repo() -> DeliveryRepo:
    return DeliveryRepo()


@pytest.fixture()
def example_delivery() -> Delivery:
    return Delivery(
        id=uuid4(),
        title='Example Delivery',
        description='Delivery description',
        status=DeliveryStatuses.ACTIVATE,
        user_id=uuid4()
    )


def test_get_deliverys_empty(delivery_repo: DeliveryRepo):
    deliverys = delivery_repo.get_deliverys()
    assert len(deliverys) == 0


def test_create_delivery(delivery_repo: DeliveryRepo, example_delivery: Delivery):
    created_delivery = delivery_repo.create_delivery(example_delivery)
    assert created_delivery in delivery_repo.get_deliverys()


def test_create_duplicate_delivery_error(delivery_repo: DeliveryRepo, example_delivery: Delivery):
    delivery_repo.create_delivery(example_delivery)
    with pytest.raises(KeyError):
        delivery_repo.create_delivery(example_delivery)


def test_done_delivery(delivery_repo: DeliveryRepo, example_delivery: Delivery):
    created_delivery = delivery_repo.create_delivery(example_delivery)
    updated_delivery = delivery_repo.done_delivery(created_delivery)
    assert updated_delivery.status == DeliveryStatuses.DONE
    assert updated_delivery in delivery_repo.get_deliverys()


def test_get_delivery_by_id(delivery_repo: DeliveryRepo, example_delivery: Delivery):
    created_delivery = delivery_repo.create_delivery(example_delivery)
    retrieved_delivery = delivery_repo.get_delivery_by_id(created_delivery.id)
    assert retrieved_delivery == created_delivery


def test_get_delivery_by_id_error(delivery_repo: DeliveryRepo):
    with pytest.raises(KeyError):
        delivery_repo.get_delivery_by_id(uuid4())
