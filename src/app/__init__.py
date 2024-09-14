from flask import Flask
from flask_migrate import Migrate
from .db import db
from .models import *
from .controllers import customer_controller


north_wind_app = Flask("northwind")
north_wind_app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:my-secret-pw@localhost:33061/northwind"


db.init_app(north_wind_app)
migrate = Migrate(north_wind_app, db)

north_wind_app.register_blueprint(customer_controller.customer_bp, url_prefix="/v1/customers")
