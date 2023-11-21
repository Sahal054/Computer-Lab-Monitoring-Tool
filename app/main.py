from ast import List
from fastapi import FastAPI , Depends, HTTPException
from db.database import SessionLocal, engine
from models import models
from schemas import schemas
from sqlalchemy.orm import Session



app = FastAPI()

models.Base.metadata.create_all(bind=engine)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ellam lab endpoint
@app.get("/labs", response_model=schemas.LabInfo)
async def get_labs(db: Session = Depends(get_db)):
    labs = db.query(models.LabInfo).all()
    return labs



# endpoint to get a specific lab
@app.get("/labs/{lab_id}", response_model=schemas.LabInfo)
async def get_lab(lab_id: int, db: Session = Depends(get_db)):
    lab = db.query(models.LabInfo).filter(models.LabInfo.Lab_ID == lab_id).first()
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    return lab


# endpoint to get all computers in a lab
@app.get("/labs/{lab_id}/computers", response_model=schemas.ComputerInfo)
async def get_computers(lab_id: int, db: Session = Depends(get_db)):
    computers = db.query(models.ComputerInfo).filter(models.ComputerInfo.Lab_ID == lab_id).all()
    return computers


# endpoint to get a specific computer in a lab
@app.get("/labs/{lab_id}/computers/{computer_id}", response_model=schemas.ComputerInfo)
async def get_computer(lab_id: int, computer_id: int, db: Session = Depends(get_db)):
    computer = db.query(models.ComputerInfo).filter(
        models.ComputerInfo.Lab_ID == lab_id, models.ComputerInfo.Computer_ID == computer_id
    ).first()
    if not computer:
        raise HTTPException(status_code=404, detail="Computer not found")
    return computer


# endpoint to get network information for a lab
@app.get("/labs/{lab_id}/network", response_model=schemas.NetworkInfo)
async def get_network_info(lab_id: int, db: Session = Depends(get_db)):
    network_info = db.query(models.NetworkInfo).filter(models.NetworkInfo.Lab_ID == lab_id).first()
    if not network_info:
        raise HTTPException(status_code=404, detail="Network information not found")
    return network_info


# endpoint to get software information for a specific computer
@app.get("/labs/{lab_id}/computers/{computer_id}/software", response_model=schemas.SoftwareInfo)
async def get_software_info(lab_id: int, computer_id: int, db: Session = Depends(get_db)):
    software_info = db.query(models.SoftwareInfo).filter(
        models.SoftwareInfo.Computer_ID == computer_id
    ).all()
    return software_info


# endpoint to get all alerts
@app.get("/alerts", response_model=schemas.Alerts)
async def get_alerts(db: Session = Depends(get_db)):
    alerts = db.query(models.Alerts).all()
    return alerts


# endpoint to get a specific alert (chumma irikiathe )
@app.get("/alerts/{alert_id}", response_model=schemas.Alerts)
async def get_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(models.Alerts).filter(models.Alerts.Alert_ID == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert
 # endpoint to create an alert (ithum chumma irikathe changes vertham udayupu anne)
@app.post("/alerts", response_model=schemas.Alerts)
async def create_alert(alert: schemas.Alerts, db: Session = Depends(get_db)):
    new_alert = models.Alerts(
        Lab_ID=alert.Lab_ID,
        Computer_ID=alert.Computer_ID,
        Network_ID=alert.Network_ID,
        Alert_Type=alert.Alert_Type,
        Alert_Description=alert.Alert_Description,
        Alert_Timestamp=alert.Alert_Timestamp,
    )

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    return new_alert