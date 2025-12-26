from sqlalchemy import Column, String, Date
from .base import Base


class Merchant(Base):
    __table_args__ = {"schema": "data_engineering_1_2"}
    __tablename__ = "merchants"

    merchant_id = Column(String(100), primary_key=True)
    merchant_name = Column(String(300), nullable=False)
    type = Column(String(100), nullable=False)
    date = Column(Date, nullable=False)
