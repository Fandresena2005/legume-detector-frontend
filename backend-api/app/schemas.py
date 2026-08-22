from typing import Optional
from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    status: str = "success"
    prediction: str = Field(..., description="Classe prédite, ex: 'sain' ou 'pourri'")
    confidence: float = Field(..., ge=0, le=100, description="Confiance en pourcentage")
    probabilities: Optional[dict] = Field(
        default=None, description="Probabilité de chaque classe en pourcentage"
    )


class ErrorResponse(BaseModel):
    status: str = "error"
    message: str


class RootResponse(BaseModel):
    message: str = "Fruit & Vegetable Detection API"
    status: str = "running"
