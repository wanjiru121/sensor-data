from fastapi import FastAPI
from app import database
from app.routes import router as sensor_router
from app import models

# Create DB tables if they don't exist
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="IoT Sensor Ingestion API",
    description="Receives and retrieves sensor data asynchronously.",
    version="1.0.0"
)

app.include_router(sensor_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
