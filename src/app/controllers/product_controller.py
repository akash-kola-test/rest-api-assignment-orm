import logging
from sqlalchemy.orm import selectinload, joinedload
from flask import Blueprint, request
from ..models import Product
from ..db import db

product_bp = Blueprint("products", __name__)
logger = logging.getLogger("northwind")

@product_bp.get("/")
def get_all_products():
    page = int(request.args.get("page", 1))
    if page <= 0:
        return "invalid page", 400

    print(f"page number is {page}",)
    print(f"offset number is {(page - 1) * 10}")

    products = (Product.query.limit(10).offset((page - 1)  * 10)
                .options(selectinload(Product.category), selectinload(Product.supplier))
                .all())
    product_dicts = []
    for product in products:
        product_dict = product.to_dict()
        product_dict["category"] = product.category.to_dict() if product.category else None
        product_dict["supplier"] = product.supplier.to_dict() if product.supplier else None
        product_dicts.append(product_dict)

    return product_dicts

@product_bp.get("/<int:product_id>")
def get_product(product_id):
    product = Product.query.options(joinedload(Product.category), joinedload(Product.supplier)).get(product_id)
    # product = Product.query.get(product_id)
    if product is None:
        return f"product not found with id {product_id}", 404

    product_dict = product.to_dict()
    product_dict["category"] = product.category.to_dict() if product.category else None
    product_dict["supplier"] = product.supplier.to_dict() if product.supplier else None

    return product_dict


@product_bp.post("/")
def add_product():
    data = request.json
    required_fields = ['product_name', 'quantity_per_unit', 'discontinued']
    for field in required_fields:
        if field not in data:
            return {"error": f"Missing required field: {field}"}, 400

    new_product = Product(
        product_name=data['product_name'],
        supplier_id=data.get('supplier_id'),
        category_id=data.get('category_id'),
        quantity_per_unit=data['quantity_per_unit'],
        unit_price=data.get('unit_price'),
        units_in_stock=data.get('units_in_stock'),
        units_on_order=data.get('units_on_order'),
        reorder_level=data.get('reorder_level'),
        discontinued= 1 if data['discontinued'] == True else 0
    )

    db.session.add(new_product)
    db.session.commit()

    return {"message": f"Added {new_product.product_name} successfully!"}


@product_bp.patch("/<product_id>")
def update_product(product_id):
    data = request.json
    existing_product = Product.query.get(product_id)

    if not existing_product:
        return f"Product not found with id {product_id}", 404

    for key, value in data.items():
        if hasattr(existing_product, key):
            setattr(existing_product, key, value)

    db.session.commit()

    return {"message": f"Updated product {existing_product.product_name} successfully!"}

