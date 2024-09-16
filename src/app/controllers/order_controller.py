from datetime import datetime
from sqlalchemy.orm import joinedload, dynamic_loader, selectinload
from flask import Blueprint, request
from ..models import Order
from ..db import db

order_bp = Blueprint("orders", __name__)


@order_bp.get("/")
def get_all_orders():
    page = int(request.args.get("page", 1))
    if page <= 0:
        return "invalid page", 400

    orders = (Order.query.limit(10).offset((page - 1)  * 10)
              .options(
                selectinload(Order.customer),
                selectinload(Order.employee),
                selectinload(Order.shipper))
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


@order_bp.get("/<int:order_id>")
def get_order(order_id):
    order = (Order.query
             .options(
                joinedload(Order.customer),
                joinedload(Order.employee),
                joinedload(Order.shipper))
             .get(order_id))
    if order is None:
        return f"order not found with id {order_id}", 404

    order_dict = order.to_dict()
    order_dict["customer"] = order.customer.to_dict() if order.customer else None
    order_dict["employee"] = order.employee.to_dict() if order.employee else None
    order_dict["shipper"] = order.shipper.to_dict() if order.shipper else None
    order_dict["last_10_order_details"] = [order_detail.to_dict() for order_detail in order.order_details.limit(10).all()]

    return order_dict


@order_bp.post("/")
def add_order():
    data = request.json

    required_fields = ['order_date', 'ship_via']
    for field in required_fields:
        if field not in data:
            return {"error": f"Missing required field: {field}"}, 400

    order_date = data.get('order_date') if datetime.fromisoformat(data.get('order_date')) else None
    required_date = data.get('required_date') if datetime.fromisoformat(data.get('required_date')) else None
    shipped_date = data.get('shipped_date') if datetime.fromisoformat(data.get('shipped_date')) else None

    new_order = Order(
        customer_id=data.get('customer_id'),
        employee_id=data.get('employee_id'),
        order_date=order_date,
        required_date=required_date,
        shipped_date=shipped_date,
        ship_via=data['ship_via'],
        freight=data.get('freight'),
        ship_name=data.get('ship_name'),
        ship_address=data.get('ship_address'),
        ship_city=data.get('ship_city'),
        ship_region=data.get('ship_region'),
        ship_postal_code=data.get('ship_postal_code'),
        ship_country=data.get('ship_country')
    )

    db.session.add(new_order)
    db.session.commit()

    return {"message": f"Added order #{new_order.order_id} successfully!"}


@order_bp.patch("/<order_id>")
def update_order(order_id):
    data = request.json
    existing_order = Order.query.get(order_id)

    if not existing_order:
        return f"order not found with id {order_id}", 404

    for key, value in data.items():
        if hasattr(existing_order, key):
            setattr(existing_order, key, value)

    db.session.commit()

    return {"message": f"Updated order #{existing_order.order_id} successfully!"}

