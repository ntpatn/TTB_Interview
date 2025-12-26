from fastapi import FastAPI
from routers import prediction

app = FastAPI(
    title="Data Engineering TTB Interview",
    description="API for Question 4: Create a FastAPI endpoint POST/predict",
    version="1.0.0",
)


@app.get("/", tags=["Health Check"])
def root():
    return {"status": "API is running"}


app.include_router(prediction.router)
