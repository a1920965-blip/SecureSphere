from fastapi import Form
from pydantic import BaseModel
from datetime import datetime
from typing import Optional,List


class UserAuth(BaseModel):
    user_id:str
    password:str
    @classmethod
    def as_form(cls,user_id:str=Form(...),password:str=Form(...)):
        return cls(user_id=user_id,password=password)

class NewUser(UserAuth):
    contact:str
    email:str
    name:str
    @classmethod
    def as_form(
        cls,
        user_id:str=Form(...),
        password:str=Form(...),
        contact:str=Form(...),
        email:str=Form(...),
        name:str=Form(...)):
        return cls(user_id=user_id,password=password,contact=contact,email=email,name=name)
class UserOut(BaseModel):
    user_id:str
    email:str
    contact:str



