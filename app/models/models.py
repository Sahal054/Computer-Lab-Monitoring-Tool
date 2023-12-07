
from sqlalchemy import Column, Integer, MetaData, String, Enum, DateTime, ForeignKey, Text
from datetime import datetime
from db.database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LabInfo(Base):
    __tablename__ = "Lab_Info"
    Lab_ID: int = Column(Integer, primary_key=True, autoincrement=True)
    Lab_Name: str = Column(String(255), nullable=False)
    Lab_Location: str = Column(String(255), nullable=False)
    Lab_Capacity: int = Column(Integer, nullable=False)

class ComputerInfo(Base):
    __tablename__ = "ComputerInfo"
    Computer_ID: int = Column(Integer, primary_key=True, autoincrement=True)
    Lab_ID: int = Column(Integer, ForeignKey(LabInfo.Lab_ID), nullable=False)
    Computer_Name: str = Column(String(255), nullable=False)
    Computer_Status: str = Column(String(255), nullable=False)
    Last_Heartbeat: DateTime = Column(DateTime,default=datetime.utcnow)

class NetworkInfo(Base):
    __tablename__ = "NetworkInfo"    
    Network_ID: int = Column(Integer, primary_key=True, autoincrement=True)
    Lab_ID: int = Column(Integer, ForeignKey(LabInfo.Lab_ID), nullable=False)
    Network_Name: str = Column(String(255), nullable=False)
    Network_Status: str = Column(String(255), nullable=False)
    Last_Check: DateTime = Column(DateTime,default=datetime.utcnow)

class SoftwareInfo(Base):
    __tablename__ = "SoftwareInfo" 
    Software_ID: int = Column(Integer, primary_key=True, autoincrement=True)
    Computer_ID: int = Column(Integer, ForeignKey(ComputerInfo.Computer_ID), nullable=False)
    Software_Name: str = Column(String(255), nullable=False)
    Software_Version: str = Column(String(255), nullable=False)

class Alerts(Base):
    __tablename__ = "Alerts" 
    Alert_ID: int = Column(Integer, primary_key=True, autoincrement=True)
    Lab_ID: int = Column(Integer, ForeignKey(LabInfo.Lab_ID))
    Computer_ID: int = Column(Integer, ForeignKey(ComputerInfo.Computer_ID))
    Network_ID: int = Column(Integer, ForeignKey(NetworkInfo.Network_ID))
    Alert_Type: str = Column(String(255), nullable=False)
    Alert_Description: str = Column(Text, nullable=False)
    Alert_Timestamp: DateTime = Column(DateTime, default=datetime.utcnow)
    


class Users(Base):
    __tablename__ = "Users" 
    User_ID: int = Column(Integer, primary_key=True, autoincrement=True)
    Username: str = Column(String(255), unique=True, nullable=False)
    Password: str = Column(String(255), nullable=False)
    Email: str = Column(String(255), unique=True, nullable=False)
    Role: str = Column(Enum('admin', 'user'), nullable=False)

    
