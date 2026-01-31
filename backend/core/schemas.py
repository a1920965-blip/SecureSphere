from fastapi import Form
from pydantic import BaseModel
from datetime import datetime
from typing import Optional,List



#-------------------------auth----------------------------------------------------------------------------------------#
class Validate_login(BaseModel):
    user_id:str
    password:str
    def as_form(cls,user_id:str=Form(...),
                    password:str=Form(...)):
        return cls(user_id=user_id,password=password)

class Validate_user_registration(Validate_login):
    contact:str
    email:str
    name:str
    def as_form(cls,user_id:str=Form(...),
                    password:str=Form(...),
                    contact:str=Form(...),
                    email:str=Form(...),
                    name:str=Form(...)):
        return cls(contact=contact,name=name,email=email,user_id=user_id,password=password)
class LoginOut(BaseModel):
    user_id:str
    status:bool
    token:str


#----------------------------------------USER SCEHMAS---------------------------------------------------------------#
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

class Add_vehicle(BaseModel):
    number:str

class Delete_vehicle(BaseModel):
    number:str

         #---------------------------USER SUPPORT SCHEMAS--------------------#

class Complaint_post(BaseModel):
    category:str
    description:str
    subject:str
    attachment:str
class Epass_post(BaseModel):
    user_id:str
    vehicle_no:Optional[str]
    contact:str
    name:str
    purpose:Optional[str]
    arrival:Optional[str]="Not Specified"
    departure:Optional[str]="Not Specified"



#------------------------------------------------ADMIN SCHEMAS-------------------------------------------------------#
class Complaint_update(BaseModel):
    user_id:str
    category:str   
    description:str
    subject:Optional[str]=None
    attachment:Optional[str]=None
    status:str
    remark:Optional[str]=None
    
class Epass_update(BaseModel):
    guest_name:str
    purpose:str
    arrival:str
    departure:str
    contact:str
    vehicle_no:Optional[str]=None
    status:str
    remark:Optional[str]=None




#---------------------------------------Response Model--------------------------------------------#
class User_registration_response(BaseModel):
    status:bool
    message:str
