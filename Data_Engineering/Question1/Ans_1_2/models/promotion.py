from sqlalchemy import Column, Integer, String, Date, ForeignKey
from .base import Base


class Promotion(Base):
    __table_args__ = {"schema": "data_engineering_1_2"}
    __tablename__ = "promotions"

    promotion_id = Column(Integer, primary_key=True)
    promotion_name = Column(String(300), nullable=False)
    merchant_id = Column(
        String(100),
        ForeignKey("data_engineering_1_2.merchants.merchant_id"),
        nullable=False,
    )
    req_point = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
