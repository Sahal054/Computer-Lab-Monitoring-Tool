import datetime
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .db.database import SessionLocal, engine
from app.models import models
from app.schemas import schemas
from fastapi.staticfiles import StaticFiles

# Create FastAPI instance
app = FastAPI()
#app.mount("/templates", StaticFiles(directory="templates"), name="templates")
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create templates instance
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def render_labs(request: Request):
    try:
        return templates.TemplateResponse("home.html", {"request": request})
    except Exception as e:
        print(f"Error rendering labs.html: {e}")
        # Handle the error appropriately
        return HTMLResponse(content="An error occurred while rendering home.html", status_code=500)

@app.get("/labs", response_class=HTMLResponse)
async def get_labs(request: Request, db: Session = Depends(get_db)):
    try:
        # Fetch labs from the database
        labs = db.query(models.LabInfo).all()

        # Render the HTML template with the fetched data
        return templates.TemplateResponse("labs.html", {"request": request, "labs": labs})
    except Exception as e:
        print(f"Error rendering labs.html: {e}")
        # Handle the error appropriately
        return HTMLResponse(content="An error occurred while rendering labs.html", status_code=500)
# ... your database setup and model definitions ...

# endpoint to get a specific lab
@app.get("/labs/{lab_id}",response_class=HTMLResponse)
async def get_lab(request: Request,lab_id: int, db: Session = Depends(get_db)):
    lab = db.query(models.LabInfo).filter(models.LabInfo.Lab_ID == lab_id).first()
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    return templates.TemplateResponse("labChosen.html", {"request": request, "lab": lab})


# endpoint to get all computers in a lab(error here)
@app.get("/labs/{lab_id}/computers",response_class=HTMLResponse)
async def get_computers(request: Request,lab_id: int, db: Session = Depends(get_db)):
    computers = db.query(models.ComputerInfo).filter(models.ComputerInfo.Lab_ID == lab_id).all()
    if not computers:
          raise HTTPException(status_code=404, detail="Lab not found")
    return templates.TemplateResponse("labComputers.html", {"request": request, "computers": computers})
    


# endpoint to get a specific computer in a lab
@app.get("/labs/{lab_id}/computers/{computer_id}", response_model=schemas.ComputerInfo)
async def get_computer(request: Request,lab_id: int, computer_id: int, db: Session = Depends(get_db)):
    computer = db.query(models.ComputerInfo).filter(
        models.ComputerInfo.Lab_ID == lab_id, models.ComputerInfo.Computer_ID == computer_id
    ).first()
    if not computer:
        raise HTTPException(status_code=404, detail="Computer not found")
    return computer



# endpoint to get network information for a lab
@app.get("/labs/{lab_id}/network",response_class=HTMLResponse )
async def get_network_info(request: Request,lab_id: int, db: Session = Depends(get_db)):
    network_info = db.query(models.NetworkInfo).filter(models.NetworkInfo.Lab_ID == lab_id).first()
    if not network_info:
        raise HTTPException(status_code=404, detail="Network information not found")
    return templates.TemplateResponse("network.html", {"request": request, "network_data":network_info })



# endpoint to get software information for a specific computer
@app.get("/labs/{lab_id}/computers/{computer_id}/software")
async def get_software_info(lab_id: int, computer_id: int, db: Session = Depends(get_db)):
    software_info = db.query(models.SoftwareInfo).filter(
        models.SoftwareInfo.Computer_ID == computer_id
    ).all()
    return software_info


# endpoint to get all alerts
@app.get("/alerts")
async def get_alerts(db: Session = Depends(get_db)):
    alerts = db.query(models.Alerts).all()
    return alerts


# # endpoint to get a specific alert (chumma irikiathe )
# @app.get("/alerts/{alert_id}", response_model=schemas.Alerts)
# async def get_alert(alert_id: int, db: Session = Depends(get_db)):
#     alert = db.query(models.Alerts).filter(models.Alerts.Alert_ID == alert_id).first()
#     if not alert:
#         raise HTTPException(status_code=404, detail="Alert not found")
#     return alert
#  # endpoint to create an alert (ithum chumma irikathe changes vertham udayupu anne)
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

#Creates New Lab
@app.post("/labs", response_model=schemas.LabInfo, status_code=201)
async def create_lab(lab: schemas.LabInfo, db: Session = Depends(get_db)):
    new_lab = models.LabInfo(
        Lab_Name=lab.Lab_Name,
        Lab_Location=lab.Lab_Location,
        Lab_Capacity=lab.Lab_Capacity,
    )

    db.add(new_lab)
    db.commit()
    db.refresh(new_lab)

    return new_lab
#Add a new Computer to a specific Lab
@app.post("/labs/{lab_id}/computers", response_model=schemas.ComputerInfo, status_code=201)
async def create_computer(lab_id: int, computer: schemas.ComputerInfo, db: Session = Depends(get_db)):
    new_computer = models.ComputerInfo(
        Lab_ID=lab_id,
        Computer_Name=computer.Computer_Name,
        Computer_Status=computer.Computer_Status,
    )

    db.add(new_computer)
    db.commit()
    db.refresh(new_computer)

    return new_computer
#Add Network Information for a Lab
@app.post("/labs/{lab_id}/network", response_model=schemas.NetworkInfo, status_code=201)
async def create_network_info(lab_id: int, network: schemas.NetworkInfo, db: Session = Depends(get_db)):
    new_network_info = models.NetworkInfo(
        Lab_ID=lab_id,
        Network_Name=network.Network_Name,
        Network_Status=network.Network_Status,
    )

    db.add(new_network_info)
    db.commit()
    db.refresh(new_network_info)

    return new_network_info


#Add Software Information for a Computer

@app.post("/labs/{lab_id}/computers/{computer_id}/software", response_model=schemas.SoftwareInfo, status_code=201)
async def create_software_info(lab_id: int, computer_id: int, software: schemas.SoftwareInfo, db: Session = Depends(get_db)):
    new_software_info = models.SoftwareInfo(
        Computer_ID=computer_id,
        Software_Name=software.Software_Name,
        Software_Version=software.Software_Version,
    )

    db.add(new_software_info)
    db.commit()
    db.refresh(new_software_info)

    return new_software_info


# To Update Network Status
@app.put("/labs/{lab_id}/network", response_model=schemas.NetworkInfo, status_code=200)
async def update_network_status(lab_id: int, network: schemas.NetworkInfo, db: Session = Depends(get_db)):
    existing_network_info = db.query(models.NetworkInfo).filter(models.NetworkInfo.Lab_ID == lab_id).first()

    if not existing_network_info:
        raise HTTPException(status_code=404, detail="Network information not found for this lab")

    existing_network_info.Network_Status = network.Network_Status
    existing_network_info.Last_Check = network.Last_Check

    db.commit()

    return existing_network_info



async def scan_and_manage_network_alerts(db: Session):
    # Get all network information
    network_infos = db.query(models.NetworkInfo).all()

    for network_info in network_infos:
        # Check current network status
        is_down = network_info.Network_Status == "down"

        # Get existing alerts for this network
        alerts = db.query(models.Alerts).filter(
            models.Alerts.Network_ID == network_info.Network_ID, models.Alerts.Alert_Type == "NetworkDown"
        )

        # Handle network down scenario
        if is_down:
            # Check if an alert already exists
            alert_exists = alerts.first()

            if not alert_exists:
                # Create a new alert
                new_alert = models.Alerts(
                    Lab_ID=network_info.Lab_ID,
                    Network_ID=network_info.Network_ID,
                    Alert_Type="NetworkDown",
                    Alert_Description=f"Network in lab {network_info.Lab_ID} is down",
                    Alert_Timestamp=datetime.now(),
                )
                db.add(new_alert)

        # Handle network up scenario (if alerts exist)
        elif alerts.exists():
            # Delete all existing network down alerts
            for alert in alerts:
                db.delete(alert)

    # Commit changes to the database
    db.commit()