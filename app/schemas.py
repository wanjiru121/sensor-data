from pydantic import BaseModel, Field, validator
from datetime import datetime, timezone

class SensorReadingCreate(BaseModel):
    device_id: str
    temperature: float = Field(..., ge=-50, le=150)
    humidity: float = Field(..., ge=0, le=100)
    timestamp: datetime

    @validator("device_id")
    def validate_device_id(cls, v):
        if not v.startswith("sensor-"):
            raise ValueError("device_id must start with 'sensor-'")
        return v

    @validator("timestamp")
    def validate_timestamp(cls, v):
        now = datetime.now(timezone.utc)
        if v > now:
            raise ValueError("Timestamp cannot be in the future")
        return v

class SensorReadingResponse(BaseModel):
    id: int
    device_id: str
    temperature: float
    humidity: float
    timestamp: datetime

    class Config:
        from_attributes = True
