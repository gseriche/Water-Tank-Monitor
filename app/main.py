from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import models
import schemas
from database import engine, Base, get_db

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/measurements", response_model=schemas.MeasurementResponse)
def create_measurement(measurement: schemas.MeasurementCreate, db: Session = Depends(get_db)):
    new_measurement = models.Measurement(liters=measurement.liters)
    db.add(new_measurement)
    db.commit()
    db.refresh(new_measurement)
    return new_measurement

@app.get("/stats")
def get_status(db: Session = Depends(get_db)):
    measurements = db.query(models.Measurement).order_by(models.Measurement.timestamp).all()
    if len(measurements) < 2:
        raise HTTPException(status_code=400, detail="Not enough data to calculate stats")
    
    total_consumption = measurements[0].liters - measurements[-1].liters
    total_time = (measurements[-1].timestamp - measurements[0].timestamp).total_seconds() / 3600
    consumption_per_hour = total_consumption / total_time if total_time > 0 else 0
    days_to_critical = (measurements[-1].liters - 200) / (consumption_per_hour * 24) if consumption_per_hour > 0 else 0

    return {
        "consumption_per_hour": round(consumption_per_hour, 2),
        "days_to_critical": round(days_to_critical, 2)
    }
