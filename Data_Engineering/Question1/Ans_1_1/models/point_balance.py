from sqlalchemy import Column, Integer, String, Date, ForeignKey
from .base import Base


class PointBalance(Base):
    __table_args__ = {"schema": "data_engineering_1_1"}
    __tablename__ = "point_balance"

    customer_id = Column(
        String(100),
        ForeignKey("data_engineering_1_1.customers.customer_id"),
        primary_key=True,
        nullable=False,
    )
    point_balance_date = Column(Date, nullable=False)
    point_balance = Column(Integer, nullable=False)
