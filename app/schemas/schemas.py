from enum import Enum
from typing import List
from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    User_ID: int
    Username: str
    Password: str
    Email: str
    Role: str = Enum('admin', 'user')

class LabInfo(BaseModel):
    Lab_ID: int
    Lab_Name: str
    Lab_Location: str
    Lab_Capacity: int

class ComputerInfo(BaseModel):
    Computer_ID: int
    Lab_ID: int
    Computer_Name: str
    Computer_Status: str = Enum('available', 'in_use')
    Last_Heartbeat: datetime

class NetworkInfo(BaseModel):
    Network_ID: int
    Lab_ID: int
    Network_Name: str
    Network_Status: str = Enum('up', 'down')
    Last_Check: datetime

class SoftwareInfo(BaseModel):
    Software_ID: int
    Computer_ID: int
    Software_Name: str
    Software_Version: str

class Alerts(BaseModel):
    Alert_ID: int
    Lab_ID: int
    Computer_ID: int
    Network_ID: int
    Alert_Type: str
    Alert_Description: str
    Alert_Timestamp: str

class LabWithAlerts(BaseModel):
    lab_info: LabInfo
    alerts: List[Alerts]

class NetworkAlertStatus(BaseModel):
    alert_status: str
    alert_message: str


