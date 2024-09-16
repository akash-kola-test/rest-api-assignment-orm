from flask import Blueprint, request
from sqlalchemy.orm import joinedload
from ..models import Customer, Order
from ..db import db

customer_bp = Blueprint("customers", __name__)


@customer_bp.get("/")
def get_all_customers():
    page = int(request.args.get("page", 1))
    if page <= 0:
        return "invalid page", 400

    customers = Customer.query.limit(10).offset((page - 1)  * 10).all()
    return [customer.to_dict() for customer in customers]


@customer_bp.get("/<customer_id>")
def get_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return f"customer not found with id {customer_id}", 404

    return customer.to_dict()


@customer_bp.post("/")
def add_customer():
    data = request.json

    if (not data.get('customer_id')
            or len(data.get('customer_id')) == 0
            or not data.get('company_name')
            or len(data.get('company_name')) == 0):

        return "Customer ID and Company Name are required.", 400

    if Customer.query.get(data.get('customer_id')):
        return f"Customer already exists with id {data.get('customer_id')}", 400

    new_customer = Customer(
        customer_id=data.get('customer_id'),
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

    db.session.add(new_customer)
    db.session.commit()

    return {"message": f"Added {new_customer.company_name} successfully!"}


@customer_bp.patch("/<customer_id>")
def update_customer(customer_id):
    data = request.json
    existing_customer = Customer.query.get(customer_id)

    if not existing_customer:
        return f"Customer not found with id {customer_id}", 404

    for key, value in data.items():
        if hasattr(existing_customer, key):
            setattr(existing_customer, key, value)

    db.session.commit()
    return {"message": f"Updated customer {existing_customer.company_name} successfully!"}


@customer_bp.get("/<customer_id>/orders")
def get_customer_orders(customer_id):
    page = int(request.args.get("page", 1))
    orders = (Order.query.filter_by(customer_id = customer_id)
                .options(
                    joinedload(Order.customer),
                    joinedload(Order.employee),
                    joinedload(Order.shipper))
                .limit(10)
                .offset((page - 1) * 10)
                .all())

    orders_dict = []
    for order in orders:
        order_dict = order.to_dict()
        order_dict["customer"] = order.customer.to_dict() if order.customer else None
        order_dict["employee"] = order.employee.to_dict() if order.employee else None
        order_dict["shipper"] = order.shipper.to_dict() if order.shipper else None
        order_dict["last_10_order_details"] = [order_detail.to_dict() for order_detail in order.order_details.limit(10).all()]
        orders_dict.append(order_dict)

    return orders_dict
