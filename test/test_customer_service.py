from unittest.mock import patch, Mock

import pytest

from app.exceptions import InvalidPageException, InvalidResourceIdException
from app.models import Customer
from app.services import customer_service


@patch("app.repositories.customer_repository.get_customers")
def test_get_all_customers(get_customers_mock: Mock):
    expected_customers = [Customer(customer_id="Hello", company_name="Test")]
    get_customers_mock.return_value = expected_customers

    customers = customer_service.get_all_customers()

    assert len(customers) == 1
    assert [customer.to_dict() for customer in expected_customers] == customers
    get_customers_mock.assert_called_once_with(1, 15)


def test_get_all_customers_fails_if_page_is_not_a_number():
    page = "hello"

    with pytest.raises(InvalidPageException) as exc_info:
        customer_service.get_all_customers(page=page)

    assert exc_info.value.msg == f"Invalid page {page}, page should be a number starting from 1"


def test_get_all_customers_fails_if_page_is_invalid_number():
    page = "-1"

    with pytest.raises(InvalidPageException) as exc_info:
        customer_service.get_all_customers(page=page)

    assert exc_info.value.msg == f"Invalid page {page}, page should be a number starting from 1"


@patch("app.repositories.customer_repository.get_customer")
def test_get_customer(get_customer_mock: Mock):
    customer_id = "test"
    expected_customer = Customer(customer_id=customer_id, company_name="Test")
    get_customer_mock.return_value = expected_customer

    customer = customer_service.get_customer(customer_id)

    assert expected_customer.to_dict() == customer
    get_customer_mock.assert_called_once_with(customer_id)


def test_get_customer_fails_with_invalid_customer_id():
    invalid_customer_id_1 = ""
    invalid_customer_id_2 = None

    with pytest.raises(InvalidResourceIdException) as exc_info_1:
        customer_service.get_customer(invalid_customer_id_1)

    with pytest.raises(InvalidResourceIdException) as exc_info_2:
        customer_service.get_customer(invalid_customer_id_2) # type: ignore

    assert exc_info_1.value.msg == f"Requested customer id {invalid_customer_id_1} is invalid"
    assert exc_info_2.value.msg == f"Requested customer id {invalid_customer_id_2} is invalid"

