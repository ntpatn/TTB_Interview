from sqlalchemy import Column, String, Date, Float, ForeignKey
from .base import Base


class CCTransaction(Base):
    __table_args__ = {"schema": "data_engineering_1_1"}
    __tablename__ = "cc_transactions"

    transaction_id = Column(String(100), primary_key=True)
    customer_id = Column(
        String(100),
        ForeignKey("data_engineering_1_1.customers.customer_id"),
        nullable=False,
    )
    credit_card_number = Column(String(20), nullable=False)
    transaction_date = Column(Date, nullable=False)
    merchant_id = Column(String(100), nullable=False)
    transaction_amount = Column(Float, nullable=False)
