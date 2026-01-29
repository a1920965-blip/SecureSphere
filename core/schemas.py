from fastapi import Form
from pydantic import BaseModel
from datetime import datetime
from typing import Optional,List

class UserAuth(BaseModel):
    user_id:str
    password:str

class NewUser(UserAuth):
    contact:str
    email:str
    name:str
class UserOut(BaseModel):
    user_id:str
    email:str
    contact:str

class UserDetail(BaseModel):
    user_id:str
    name:str
    contact:str
    email:str
    department:str=None
    designation:str=None
    house_no:str=None
    block:str=None
    city:str=None
    pincode:str=None
    state:str=None

class Personal(BaseModel):
    name:str
    contact:str
    email:str
    department:str=None
    designation:str=None
class Resident(BaseModel):
    house_no:str=None
    block:str=None
    city:str=None
    pincode:str=None
    state:str=None 

class Vehicle(BaseModel):
    number:str

class Complaint(BaseModel):
    category:str
    description:str
    subject:str
    attachment:str
class Epass(BaseModel):
    user_id:str
    vehicle_no:Optional[str]
    contact:str
    name:str
    purpose:Optional[str]
    arrival:Optional[str]="Not Specified"
    departure:Optional[str]="Not Specified"
    
class Token(BaseModel):
    token:str







