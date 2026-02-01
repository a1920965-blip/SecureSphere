from pydantic import BaseModel
from fastapi import Form,File
from datetime import datetime
from typing import Optional,List



#-------------------------auth----------------------------------------------------------------------------------------#
class Validate_login(BaseModel):
    user_id:str
    password:str
class Validate_user_registration(Validate_login):
    contact:str
    email:str
    name:str
class LoginOut(BaseModel):
    user_id:str
    success:bool
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

         #---------------------------USER SUPPORT SCHEMAS--------------------
class Complaint_post(BaseModel):
    category:str
    description:str
    subject:str
    has_attachment: Optional[bool] = False
    attachment: Optional[str] = None

class Epass_post(BaseModel):
    vehicle_no:Optional[str]
    contact:str
    guest_name:str
    purpose:Optional[str]
    arrival:Optional[str]="Not Specified"
    departure:Optional[str]="Not Specified"



#------------------------------------------------ADMIN SCHEMAS-------------------------------------------------------#
class Validate_admin_registration(BaseModel):
    user_id:str
    password:str
    admin_key:str
class Complaint_update(BaseModel):
    status:str
    remark:Optional[str]=None
    
class Epass_update(BaseModel):
    status:str
    remark:Optional[str]=None


class Post_notice(BaseModel):
    Type:str
    body:str
    user:str

#---------------------------------------Response Model--------------------------------------------#
class User_registration_response(BaseModel):
    success:bool
    message:str
