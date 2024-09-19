from typing import List

from app.models import Customer


def get_customers(page: int, page_size: int) -> List[Customer]:
    return Customer.query.limit(page_size).offset((page - 1) * page_size).all()


def get_customer(customer_id: str) -> Customer:
    return Customer.query.get(customer_id)
