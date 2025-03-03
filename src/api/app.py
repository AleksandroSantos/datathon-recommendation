from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from src.utils.helpers import load_model
from src.monitoring.logger import log
import numpy as np

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Carregar modelo
model = load_model("data/models/recommendation_model.pkl")

class PredictionRequest(BaseModel):
    timeOnPageHistory: float
    numberOfClicksHistory: float
    scrollPercentageHistory: float
    recency_weight: float

@app.post("/predict")
async def predict(request: PredictionRequest, token: str = Depends(oauth2_scheme)):
    """
    Endpoint para previsões.
    """
    log(f"Recebida requisição: {request}")
    input_data = np.array([[request.timeOnPageHistory, request.numberOfClicksHistory, request.scrollPercentageHistory, request.recency_weight]])
    prediction = model.predict(input_data)
    return {"prediction": prediction.tolist()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)