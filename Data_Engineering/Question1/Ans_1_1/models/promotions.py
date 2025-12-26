from sqlalchemy import Column, Integer, String, Date
from .base import Base


class Promotion(Base):
    __table_args__ = {"schema": "data_engineering_1_1"}
    __tablename__ = "promotions"

    promotion_id = Column(Integer, primary_key=True)
    promotion_name = Column(String(300), nullable=False)
    merchant_id = Column(String(100), nullable=False)
    req_point = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
