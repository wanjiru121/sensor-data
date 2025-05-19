import logging

from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def create_sensor_reading(db: Session, reading: schemas.SensorReadingCreate):
    """
    Attempts to create a new sensor reading in the database.

    If a duplicate reading is detected (based on device ID, temperature,
    humidity, and timestamp), it is skipped and a warning is logged.

    Args:
        db (Session): SQLAlchemy database session.
        reading (SensorReadingCreate): The sensor data to be saved.

    Returns:
        None
    """
    try:
        sensor_reading = models.SensorReading(**reading.dict())
        db.add(sensor_reading)
        db.commit()
        db.refresh(sensor_reading)
        logger.info(f"Sensor reading saved: {sensor_reading.device_id} @ {sensor_reading.timestamp}")
    except IntegrityError:
        db.rollback()
        logger.warning(
            f"Duplicate sensor reading skipped for device: {reading.device_id} at {reading.timestamp}"
        )


def get_latest_readings(db: Session, device_id: str, limit: int = 10):
    """
    Retrieves the most recent sensor readings for a given device.

    Args:
        db (Session): SQLAlchemy database session.
        device_id (str): The ID of the sensor device.
        limit (int, optional): The maximum number of readings to return. Defaults to 10.

    Returns:
        List[SensorReading]: A list of sensor readings ordered by newest first.
    """
    return (
        db.query(models.SensorReading)
        .filter(models.SensorReading.device_id == device_id)
        .order_by(models.SensorReading.timestamp.desc())
        .limit(limit)
        .all()
    )

