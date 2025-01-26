from pydantic import ConfigDict, BaseModel
from datetime import datetime

class MeasurementCreate(BaseModel):
    liters: float

class MeasurementResponse(BaseModel):
    id: int
    liters: float
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)