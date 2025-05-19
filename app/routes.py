from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, crud

from app.dependecies import get_db

router = APIRouter()

@router.post("/sensor-data", status_code=status.HTTP_202_ACCEPTED)
async def receive_sensor_data(
    reading: schemas.SensorReadingCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Receive and asynchronously process a new sensor reading.

    This endpoint accepts a JSON payload representing a single sensor reading,
    validates the data using Pydantic, and queues it for background processing
    to be stored in the database.

    Args:
        reading (SensorReadingCreate): The incoming sensor data payload.
        background_tasks (BackgroundTasks): FastAPI's background task handler.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: A message indicating the reading was accepted and is being processed.
    """
    background_tasks.add_task(crud.create_sensor_reading, db, reading)
    return {"message": "Reading received and being processed"}


@router.get("/sensor-data/{device_id}", response_model=list[schemas.SensorReadingResponse])
def get_sensor_data(
    device_id: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Retrieve the most recent sensor readings for a given device.

    Args:
        device_id (str): The unique identifier of the sensor device.
        limit (int, optional): The number of recent readings to return. 
                               Defaults to 10. Maximum allowed is 100.
        db (Session): Database session dependency.

    Returns:
        List[SensorReadingResponse]: A list of the latest sensor readings 
                                     for the specified device.

    Raises:
        HTTPException: If the requested limit exceeds 100.
    """
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit cannot exceed 100")
    
    readings = crud.get_latest_readings(db, device_id=device_id, limit=limit)
    return readings

