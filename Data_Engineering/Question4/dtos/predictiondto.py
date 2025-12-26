from pydantic import BaseModel

class PredictionOutput(BaseModel):
    customer_id: str
    prediction: str
    confidence: float