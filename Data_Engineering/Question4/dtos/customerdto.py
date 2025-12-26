from pydantic import BaseModel


class CustomerFeatures(BaseModel):
    age: int
    income: float
    avg_monthly_spend: float


class CustomerInput(BaseModel):
    customer_id: str
    features: CustomerFeatures
