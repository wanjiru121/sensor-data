from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, crud, database

router = APIRouter()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/sensor-data", status_code=status.HTTP_202_ACCEPTED)
async def receive_sensor_data(
    reading: schemas.SensorReadingCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Background task to store data
    background_tasks.add_task(crud.create_sensor_reading, db, reading)
    return {"message": "Reading received and being processed"}


@router.get("/sensor-data/{device_id}", response_model=list[schemas.SensorReadingResponse])
def get_sensor_data(
    device_id: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit cannot exceed 100")
    
    readings = crud.get_latest_readings(db, device_id=device_id, limit=limit)
    return readings
