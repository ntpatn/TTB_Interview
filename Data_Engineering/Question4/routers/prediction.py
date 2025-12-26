from fastapi import APIRouter, HTTPException
from dtos.customerdto import CustomerInput
from dtos.predictiondto import PredictionOutput
from services.service import service

router = APIRouter()


@router.post("/predict", response_model=PredictionOutput, tags=["Question 4"])
async def predict(data: CustomerInput):
    try:
        result = service.predict(
            age=data.features.age,
            income=data.features.income,
            spend=data.features.avg_monthly_spend,
        )

        return {
            "customer_id": data.customer_id,
            "prediction": result["prediction"],
            "confidence": result["confidence"],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
