from sqlalchemy import Column,Integer,String,TIMESTAMP,text,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Base=declarative_base()

class Auth(Base):
    __tablename__="auth"
    user_id=Column(String,nullable=False,unique=True,primary_key=True)
    password=Column(String,nullable=False)
    resident=relationship("Resident",cascade="all,delete")
    vehicle=relationship("Vehicle",cascade="all,delete")
    personal=relationship("Personal",cascade="all,delete")
    complaint=relationship("Complaint",cascade="all,delete")

class Resident(Base):
    __tablename__="resident"
    house_no=Column(String)
    block=Column(String)
    state=Column(String)
    city=Column(String)
    pincode=Column(String)
    owner=Column(String,ForeignKey("auth.user_id",ondelete="CASCADE"),nullable=False,primary_key=True)
class Personal(Base):
    __tablename__="personal"
    user_id=Column(String,ForeignKey("auth.user_id",ondelete="CASCADE"),nullable=False,primary_key=True)
    email=Column(String,nullable=False)
    Name=Column(String,nullable=False)
    department=Column(String)
    contact=Column(String,nullable=False)
    designation=Column(String)
    timestamp=Column(TIMESTAMP,server_default=text("now()"),nullable=False)
class Vehicle(Base):
    __tablename__="vehicle"
    owner=Column(String,ForeignKey("auth.user_id",ondelete="CASCADE"),nullable=False,primary_key=True)
    number=Column(String,nullable=False,primary_key=True)
    
class Complaint(Base):
    __tablename__="complaint"
    user_id=Column(String,ForeignKey("auth.user_id",ondelete="CASCADE"),nullable=False)
    complaint_id=Column(Integer,primary_key=True,index=True)
    description=Column(String,nullable=False)
    category=Column(String,nullable=False)
    attachement=Column(String)
    subject=Column(String)




