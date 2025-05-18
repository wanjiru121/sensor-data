import time
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)

# Create a fresh test DB schema before each test
@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_post_sensor_data():
    payload = {
        "device_id": "sensor-001",
        "temperature": 24.3,
        "humidity": 50.1,
        "timestamp": "2025-05-17T12:00:00Z"
    }
    response = client.post("/sensor-data", json=payload)
    assert response.status_code == 202
    assert response.json() == {"message": "Reading received and being processed"}

def test_get_sensor_data_empty():
    response = client.get("/sensor-data/sensor-001")
    assert response.status_code == 200
    assert response.json() == []

def test_get_sensor_data_after_post():
    payload = {
        "device_id": "sensor-001",
        "temperature": 26.0,
        "humidity": 47.5,
        "timestamp": "2025-05-17T13:00:00Z"
    }
    client.post("/sensor-data", json=payload)

    time.sleep(0.5)

    response = client.get("/sensor-data/sensor-001")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["device_id"] == "sensor-001"

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# ----------------------
# Error tests
# ----------------------

def test_post_missing_field():
    # Missing 'humidity'
    payload = {
        "device_id": "sensor-001",
        "temperature": 23.0,
        "timestamp": "2025-05-17T12:00:00Z"
    }
    response = client.post("/sensor-data", json=payload)
    assert response.status_code == 422

def test_post_invalid_types():
    # humidity is a string instead of float
    payload = {
        "device_id": "sensor-001",
        "temperature": 22.5,
        "humidity": "high",
        "timestamp": "2025-05-17T12:00:00Z"
    }
    response = client.post("/sensor-data", json=payload)
    assert response.status_code == 422

def test_post_invalid_timestamp():
    # Invalid timestamp format
    payload = {
        "device_id": "sensor-001",
        "temperature": 22.5,
        "humidity": 45.0,
        "timestamp": "17-05-2025 12:00"  # Invalid format
    }
    response = client.post("/sensor-data", json=payload)
    assert response.status_code == 422

def test_post_non_json_payload():
    response = client.post("/sensor-data", data="not-json")
    assert response.status_code == 422

def test_get_sensor_data_invalid_device():
    response = client.get("/sensor-data/nonexistent-device")
    assert response.status_code == 200
    assert response.json() == []
