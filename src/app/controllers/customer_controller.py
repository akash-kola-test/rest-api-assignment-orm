import logging

from flask import Blueprint, request
from ..exceptions import *
from . import customer_service

customer_bp = Blueprint("customers", __name__)
logger = logging.getLogger("northwind")


@customer_bp.get("/")
def get_all_customers():
    page = request.args.get("page", "1")
    try:
        return customer_service.get_all_customers(page)
    except InvalidPageException as e:
        return {"error": e.msg}, 400
    except Exception:
        logger.exception("Something went wrong while getting all customers with page %s", page)
        return {"error": "something went wrong"}, 500


@customer_bp.get("/<customer_id>")
def get_customer(customer_id):
    try:
        return customer_service.get_customer(customer_id)
    except (InvalidResourceIdException, ResourceNotFoundException) as e:
        return {"error": e.msg}, 400
    except Exception:
        logger.exception("Something went wrong while fetching customer information with customer_id %s", customer_id)
        return {"error": "something went wrong"}, 500


@customer_bp.post("/")
def add_customer():
    try:
        data = request.json
        customer_service.add_customer(data)
        return {"message": "customer added successfully"}
    except (ResourceAlreadyExistsException, ValidationException) as e:
        return {"error": e.msg}, 400
    except Exception:
        logger.exception("Something went wrong while adding customer")
        return {"error": "something went wrong"}, 500


@customer_bp.patch("/<customer_id>")
def update_customer(customer_id):
    try:
        data = request.json
        customer_service.update_customer(data, customer_id)
        return {"message": "customer updated successfully"}
    except ResourceNotFoundException as e:
        return {"error": e.msg}, 400
    except Exception:
        logger.exception("Something went wrong while updating customer")
        return {"error": "something went wrong"}, 500

@customer_bp.get("/<customer_id>/orders")
def get_customer_orders(customer_id):
    page = request.args.get("page", "1")
    try:
        return customer_service.get_customer_orders(customer_id, page)
    except (InvalidPageException, ResourceNotFoundException) as e:
        return {"error": e.msg}, 400
    except Exception as e:
        logger.exception("Something went wrong while fetching customer %s orders for page %s", customer_id, page)
        return {"error": "something went wrong"}, 500

