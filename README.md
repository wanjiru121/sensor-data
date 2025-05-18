# 🌡️ Sensor Data API (FastAPI + Docker)

A FastAPI microservice for receiving and querying sensor data (temperature, humidity, and timestamps) from IoT devices. It uses SQLite with SQLAlchemy and is fully containerized with Docker.

---

## 📁 Project Structure

├── app/
│ ├── main.py # FastAPI app and API routes
│ ├── models.py # SQLAlchemy ORM models
│ ├── schemas.py # Pydantic request/response models
│ ├── database.py # DB connection and session
│ ├── tasks.py # Background job handling
│ └── tests/
│ └── test_get_and_post_endpoints.py
├── data/ # SQLite database volume (mounted via Docker)
├── Dockerfile # Docker build definition
├── docker-compose.yml # Docker Compose setup
├── requirements.txt # Python dependencies
└── README.md


---

## 🐳 Run with Docker

### 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/sensor-api.git
   cd sensor-api

2. **Start the application**
    docker compose up --build

3. **Access the API**

    Swagger Docs: http://localhost:8000/docs

    Health Check: http://localhost:8000/health

### 📦 API Endpoints
- ➕ POST /sensor-data
    - Submit a new sensor reading.

        **Request Body:**
        {
            "device_id": "sensor-001",
            "temperature": 25.5,
            "humidity": 48.0,
            "timestamp": "2025-05-18T10:00:00Z"
        }

        **Response:**
        {
            "message": "Reading received and being processed"
        }

- 📊 GET /sensor-data/{device_id}
    - Retrieve all readings for a device.

    ***Response:***
    [
        {
            "device_id": "sensor-001",
            "temperature": 25.5,
            "humidity": 48.0,
            "timestamp": "2025-05-18T10:00:00Z"
        }
    ]

- ❤️ GET /health
    - Check if the service is running.

    ***Response***
    {
        "status": "ok"
    }


### 🧪 Running Tests
- Tests are written using pytest and TestClient. They cover:

    - Valid sensor data POST

    - GET before and after posting

    - Invalid inputs and edge cases

    - Health check endpoint

    - Database schema setup

    ▶️ Run Tests in Docker
        - Open a shell in the container:
            ***docker compose run web sh***

        - Run tests inside the container:
            ***pytest***

### 🛠️ Development Stack
- Language: Python 3.11

- Framework: FastAPI

- Database: SQLite (via SQLAlchemy)

- Validation: Pydantic

- Tasks: FastAPI BackgroundTasks

- Containerization: Docker, Docker Compose

- Testing: Pytest + TestClient


