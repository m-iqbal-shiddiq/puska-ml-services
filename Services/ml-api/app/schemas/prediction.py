from pydantic import BaseModel, Field
from typing import Optional


class PredictionRequest(BaseModel):
    time_type: str = Field(...,
                           description="Time type for prediction",
                           examples=["daily", "weekly"])
    id_waktu: int = Field(..., 
                          description="Date for prediction",
                          examples=[9392])
    id_lokasi: int = Field(...,
                           description="Location ID for prediction",
                           examples=[47346])
    id_unit_peternakan: Optional[int] = Field(None,
                                              description="Unit Peternakan ID for prediction",
                                              examples=[None])
    

class PredictionSuccessResponse(BaseModel):
    status: str
    message: str
    
class PredictionFailureResponse(BaseModel):
    status: str
    type: str
    message: str