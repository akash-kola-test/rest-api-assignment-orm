import logging as root_logger
from typing import List, Dict

from sqlalchemy.orm import joinedload

from app.models import Customer, Order
from app.exceptions import *
from app.db import db


logger = root_logger.getLogger("northwind")


def get_all_customers(page: str = "1", page_size: int = 15) -> List[Dict]:
    if not page.isdigit():
        logger.error("Invalid page number, and it is not a digit: %s", page)
        raise InvalidPageException(f"Invalid page {page}, page should be a number starting from 1")
    page = int(page)
    if page <= 0:
        logger.error("Invalid page number: %s", page)
        raise InvalidPageException(f"Invalid page {page}, page should be a number starting from 1")

    logger.debug("Requested page is: %s", page)
    logger.debug("Requested page size is: %s", page_size)
    customers = Customer.query.limit(page_size).offset((page - 1) * page_size).all()
    logger.debug("Returning the customers of length: %s", len(customers))

    return [customer.to_dict() for customer in customers]


def get_customer(customer_id: str) -> Dict:
    if customer_id is None or len(customer_id) is 0:
        logger.error("Requested customer id %s is invalid", customer_id)
        raise InvalidResourceIdException(f"Requested customer id {customer_id} is invalid")

    customer: Customer = Customer.query.get(customer_id)
    if customer is None:
        logger.error("customer not found with id '%s'", customer_id)
        raise ResourceNotFoundException(f"customer not found with id {customer_id}")

    logger.debug("Returning customer information with company name %s", customer.company_name)
    return customer.to_dict()

def add_customer(data) -> None:

    if (not data.get('customer_id')
            or len(str(data.get('customer_id'))) == 0
            or not data.get('company_name')
            or len(str(data.get('company_name'))) == 0):
        logger.error("Customer ID and Company Name are required fields")
        raise ValidationException("Customer ID and Company Name are required fields")

    customer_id = data.get('customer_id')

    if Customer.query.get(data.get('customer_id')):
        logger.error("Customer already exists with id %s", customer_id)
        raise ResourceAlreadyExistsException(f"Customer already exists with id {customer_id}")

    new_customer = Customer(
        customer_id=customer_id,
        company_name=data.get('company_name'),
        contact_name=data.get('contact_name'),
        contract_title=data.get('contract_title'),
        address=data.get('address'),
        city=data.get('city'),
        region=data.get('region'),
        postal_code=data.get('postal_code'),
        country=data.get('country'),
        phone=data.get('phone'),
        fax=data.get('fax'),
    )

    logger.debug("Adding new customer to the DB session")
    db.session.add(new_customer)

    logger.debug("Committing the DB changes")
    db.session.commit()

    logger.debug("Customer created successfully")


def update_customer(data, customer_id: str) -> None:
    existing_customer = Customer.query.get(customer_id)

    if not existing_customer:
        logger.error("Customer not found with id %s", customer_id)
        raise ResourceNotFoundException(f"Customer not found with id {customer_id}")

    for key, value in data.items():
        if hasattr(existing_customer, key):
            setattr(existing_customer, key, value)

    logger.debug("Committing any changes to the DB")
    db.session.commit()


def get_customer_orders(customer_id: str, page = "1", page_size: int = 15) -> List[Dict]:
    if not page.isdigit():
        logger.error("Invalid page number, and it is not a digit: %s", page)
        raise InvalidPageException(f"Invalid page {page}, page should be a number starting from 1")
    page = int(page)
    if page <= 0:
        logger.error("Invalid page number: %s", page)
        raise InvalidPageException(f"Invalid page {page}, page should be a number starting from 1")

    customer: Customer = Customer.query.get(customer_id)
    if customer is None:
        logger.error("customer not found with id '%s'", customer_id)
        raise ResourceNotFoundException(f"customer not found with id {customer_id}")

    logger.debug("fetching order for customer %s from page %s with page size %s", customer_id, page, page_size)
    orders = (Order.query
              .filter_by(customer_id=customer_id)
              .options(
                    joinedload(Order.customer),
                    joinedload(Order.employee),
                    joinedload(Order.shipper))
              .limit(page_size)
              .offset((page - 1) * page_size)
              .all())
    logger.debug("fetched %s orders for customer %s", len(orders), customer_id)

    orders_dict = []
    for order in orders:
        order_dict = order.to_dict()
        order_dict["customer"] = order.customer.to_dict() if order.customer else None
        order_dict["employee"] = order.employee.to_dict() if order.employee else None
        order_dict["shipper"] = order.shipper.to_dict() if order.shipper else None
        order_dict["last_10_order_details"] = [
            order_detail.to_dict() for order_detail in order.order_details.limit(10).all()
        ]

        orders_dict.append(order_dict)

    logger.debug("returning the orders of the requested customer %s", customer_id)
    return orders_dict

