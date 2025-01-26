import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app.models import Measurement

client = TestClient(app)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_measurement(test_db):
    response = client.post("/measurements", json={"liters": 2800})
    assert response.status_code == 200
    data = response.json()
    assert data["liters"] == 2800

# Prueba: Obtener estadísticas sin suficientes datos
def test_get_stats_not_enough_data(test_db):
    response = client.get("/stats")
    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough data to calculate stats"

# Prueba: Obtener estadísticas con datos suficientes
def test_get_stats(test_db):
    client.post("/measurements", json={"liters": 2800})
    client.post("/measurements", json={"liters": 2400})
    response = client.get("/stats")
    assert response.status_code == 200
    stats = response.json()
    assert "consumption_per_hour" in stats
    assert "days_to_critical" in stats