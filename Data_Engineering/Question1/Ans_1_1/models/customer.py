from sqlalchemy import Column, String
from .base import Base


class Customer(Base):
    __table_args__ = {"schema": "data_engineering_1_1"}
    __tablename__ = "customers"

    customer_id = Column(String(100), primary_key=True)
    name = Column(String(300), nullable=False)
