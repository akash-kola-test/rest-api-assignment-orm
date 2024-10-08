from flask import Flask
from flask_migrate import Migrate

from app.db import db
from app.models import *
from app.controllers import customer_controller, product_controller, order_controller


north_wind_app = Flask("northwind")
north_wind_app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:my-secret-pw@localhost:33061/northwind"
north_wind_app.config['SQLALCHEMY_ECHO'] = True


db.init_app(north_wind_app)
migrate = Migrate(north_wind_app, db)

north_wind_app.register_blueprint(customer_controller.customer_bp, url_prefix="/v1/customers")
north_wind_app.register_blueprint(product_controller.product_bp, url_prefix="/v1/products")
north_wind_app.register_blueprint(order_controller.order_bp, url_prefix="/v1/orders")
