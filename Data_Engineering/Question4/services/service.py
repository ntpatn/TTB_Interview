import random


class PredictService:
    def predict(self, age: int, income: float, spend: float):
        try:
            if income <= 0:
                return {
                    "prediction": "unknown",
                    "confidence": 0.0,
                }
            spend_ratio = spend / income

            prediction = "medium"
            if spend_ratio < 0.10:
                prediction = "low"
            elif 0.10 <= spend_ratio < 0.30:
                prediction = "medium"
            else:
                prediction = "high"

            confidence = round(random.uniform(0.70, 0.95), 2)

            return {"prediction": prediction, "confidence": confidence}

        except Exception as e:
            print(f"Error in calculation: {e}")
            return {"prediction": "error", "confidence": 0.0}


service = PredictService()
