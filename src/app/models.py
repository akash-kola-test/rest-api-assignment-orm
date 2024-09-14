from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, ForeignKey, CheckConstraint, Text
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .db import db


class Customer(db.Model):
    __tablename__ = "customers"

    customer_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    company_name: Mapped[str] = mapped_column(String(40))
    contact_name: Mapped[Optional[str]] = mapped_column(String(30))
    contract_title: Mapped[Optional[str]] = mapped_column(String(30))
    address: Mapped[Optional[str]] = mapped_column(String(60))
    city: Mapped[Optional[str]] = mapped_column(String(15))
    region: Mapped[Optional[str]] = mapped_column(String(15))
    postal_code: Mapped[Optional[str]] = mapped_column(String(10))
    country: Mapped[Optional[str]] = mapped_column(String(15))
    phone: Mapped[Optional[str]] = mapped_column(String(24))
    fax: Mapped[Optional[str]] = mapped_column(String(24))

    demographics: Mapped[List['CustomerDemographics']] = relationship(
        "CustomerDemographics",
        secondary="customer_customer_demo",
        back_populates="customers"
    )
    orders: Mapped[Optional[List['Order']]] = relationship(back_populates="customer")


class CustomerDemographics(db.Model):
    __tablename__ = "customer_demographics"

    customer_type_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    customer_desc: Mapped[Optional[str]] = mapped_column(String(255))

    customers: Mapped[List[Customer]] = relationship(
        "Customer",
        secondary="customer_customer_demo",
        back_populates="demographics"
    )


class CustomerDemographicsAssociation(db.Model):
    __tablename__ = "customer_customer_demo"

    customer_id: Mapped[str] = mapped_column(String(255), ForeignKey("customers.customer_id"), primary_key=True)
    customer_type_id: Mapped[str] = mapped_column(String(255), ForeignKey("customer_demographics.customer_type_id"), primary_key=True)


class Employee(db.Model):
    __tablename__ = "employees"

    employee_id: Mapped[int] = mapped_column(primary_key=True)
    last_name: Mapped[str] = mapped_column(String(20))
    first_name: Mapped[str] = mapped_column(String(10))
    title: Mapped[Optional[str]] = mapped_column(String(30))
    title_of_courtesy: Mapped[Optional[str]] = mapped_column(String(25))
    birth_date: Mapped[Optional[datetime]]
    hire_date: Mapped[Optional[datetime]]
    address: Mapped[Optional[str]] = mapped_column(String(60))
    city: Mapped[Optional[str]] = mapped_column(String(15))
    region: Mapped[Optional[str]] = mapped_column(String(15))
    postal_code: Mapped[Optional[str]] = mapped_column(String(10))
    country: Mapped[Optional[str]] = mapped_column(String(15))
    home_phone: Mapped[Optional[str]] = mapped_column(String(24))
    extension: Mapped[Optional[str]] = mapped_column(String(4))
    photo: Mapped[Optional[bytes]]
    notes: Mapped[Optional[str]] = mapped_column(String(255))
    reports_to: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.employee_id"))
    photo_path: Mapped[Optional[str]] = mapped_column(String(255))

    reporting_to: Mapped[Optional['Employee']] = relationship(remote_side=[employee_id], uselist=False)
    territories: Mapped[Optional[List['Territory']]] = relationship(secondary="employee_territories", back_populates="employees")
    orders: Mapped[Optional[List['Order']]] = relationship(back_populates="employee")


class Region(db.Model):
    __tablename__ = "region"

    region_id: Mapped[int] = mapped_column(primary_key=True)
    region_description: Mapped[str] = mapped_column(String(255))

    territories: Mapped[Optional[List['Territory']]] = relationship(back_populates="region")


class Territory(db.Model):
    __tablename__ = "territories"

    territory_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    territory_description: Mapped[str] = mapped_column(String(255))
    region_id: Mapped[int] = mapped_column(ForeignKey("region.region_id"))

    region: Mapped[Region] = relationship(back_populates="territories")
    employees: Mapped[Optional[List[Employee]]] = relationship(secondary="employee_territories", back_populates="territories")


class EmployeeTerritoryAssociation(db.Model):
    __tablename__ = "employee_territories"

    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.employee_id"), primary_key=True, )
    territory_id: Mapped[str] = mapped_column(String(255), ForeignKey("territories.territory_id"), primary_key=True)


class Category(db.Model):
    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(String(15))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    picture: Mapped[Optional[bytes]]

    products: Mapped[Optional[List['Product']]] = relationship(back_populates="category")


class Supplier(db.Model):
    __tablename__ = "suppliers"

    supplier_id: Mapped[int] = mapped_column(primary_key=True)
    company_name: Mapped[str] = mapped_column(String(40))
    contact_name: Mapped[Optional[str]] = mapped_column(String(30))
    contact_title: Mapped[Optional[str]] = mapped_column(String(30))
    address: Mapped[Optional[str]] = mapped_column(String(60))
    city: Mapped[Optional[str]] = mapped_column(String(15))
    region: Mapped[Optional[str]] = mapped_column(String(15))
    postal_code: Mapped[Optional[str]] = mapped_column(String(10))
    country: Mapped[Optional[str]] = mapped_column(String(15))
    phone: Mapped[Optional[str]] = mapped_column(String(24))
    fax: Mapped[Optional[str]] = mapped_column(String(24))
    homepage: Mapped[Optional[str]] = mapped_column(String(255))

    products: Mapped[Optional[List['Product']]] = relationship(back_populates="supplier")


class Product(db.Model):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(40))
    supplier_id: Mapped[Optional[int]] = mapped_column(ForeignKey("suppliers.supplier_id"))
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.category_id"))
    quantity_per_unit: Mapped[str] = mapped_column(String(20))
    unit_price: Mapped[Optional[float]]
    units_in_stock: Mapped[Optional[int]]
    units_on_order: Mapped[Optional[int]]
    reorder_level: Mapped[Optional[int]]
    discontinued: Mapped[int]

    category: Mapped[Optional[Category]] = relationship(back_populates="products")
    supplier: Mapped[Optional[Supplier]] = relationship(back_populates="products")


class Shipper(db.Model):
    __tablename__ = "shippers"

    shipper_id: Mapped[int] = mapped_column(primary_key=True)
    company_name: Mapped[str] = mapped_column(String(40))
    phone: Mapped[Optional[str]] = mapped_column(String(24))

    orders: Mapped[Optional[List['Order']]] = relationship(back_populates="shipper")


class Order(db.Model):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[Optional[str]] = mapped_column(String(255), ForeignKey("customers.customer_id"))
    employee_id: Mapped[Optional[int]] = mapped_column(ForeignKey("employees.employee_id"))
    order_date: Mapped[Optional[datetime]]
    required_date: Mapped[Optional[datetime]]
    shipped_date: Mapped[Optional[datetime]]
    ship_via: Mapped[str] = mapped_column(ForeignKey("shippers.shipper_id"))
    freight: Mapped[Optional[float]]
    ship_name: Mapped[Optional[str]] = mapped_column(String(40))
    ship_address: Mapped[Optional[str]] = mapped_column(String(60))
    ship_city: Mapped[Optional[str]] = mapped_column(String(15))
    ship_region: Mapped[Optional[str]] = mapped_column(String(15))
    ship_postal_code: Mapped[Optional[str]] = mapped_column(String(10))
    ship_country: Mapped[Optional[str]] = mapped_column(String(15))

    customer: Mapped[Optional[Customer]] = relationship(back_populates="orders")
    employee: Mapped[Optional[Employee]] = relationship(back_populates="orders")
    shipper: Mapped[Optional[Shipper]] = relationship(back_populates="orders")

