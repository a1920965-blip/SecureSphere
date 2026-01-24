from fastapi import Form
from pydantic import BaseModel
from datetime import datetime
from typing import Optional,List
class Register_vehicle(BaseModel):
    vehicle_no:str
    name:str
    purpose:str
    remark:Optional[str]="None"
    @classmethod
    def as_form(
        cls,
        vehicle_no:str=Form(...),
        name:str=Form(...),
        purpose:str=Form(...),
        remark:str=Form("None")
    ):
        return cls(vehicle_no=vehicle_no,name=name,purpose=purpose,remark=remark)

class Update(Register_vehicle):
    status:str
    
class Vehicle_data(BaseModel):
    vehicle_no:str
    name:str
    purpose:str
    status:str
    remark:Optional[str]=None
class RecordOut(BaseModel):
    status:bool
    data:List[Vehicle_data]
class InfoOut(BaseModel):
    status:bool
    data:Vehicle_data
class UpdateVehicle(BaseModel):
    vehicle_no: str
    status: str
    remark: str | None = None
class user_credential(BaseModel):
    user_name:str
    password:str
class NewAdminIn:
    user_name:str
    email:str
    password:str
    def as_form(
            cls,
            user_name:str=Form(...),
            email:str=Form(...),
            password:str=Form(...)
    ):
        return cls(user_name=user_name,email=email,password=password)
