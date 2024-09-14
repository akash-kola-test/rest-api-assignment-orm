from flask import Blueprint, request
from ..models import Customer

customer_bp = Blueprint("customer", __name__)


@customer_bp.get("/")
def get_all():
    page = int(request.args.get("page"))
    if page <= 0:
        return "invalid page", 400

    customers = Customer.query.limit(10).offset((page - 1)  * 10).all()
    return customers


@customer_bp.get("/<customer_id>")
def get(customer_id):
    customer = Customer.query.get(customer_id=customer_id)
    if customer is None:
        return f"customer not found with id {customer_id}", 404

    return customer


@customer_bp.post("/")
def add():
    # body = request.json()
    pass
