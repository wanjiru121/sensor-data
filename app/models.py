from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint
from .database import Base

class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    timestamp = Column(DateTime)

    __table_args__ = (
        UniqueConstraint("device_id", "temperature", "humidity", "timestamp", name="unique_sensor_reading"),
    )
