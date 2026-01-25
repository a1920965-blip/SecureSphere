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
class UserOut(BaseModel):
    user_id:str
    email:str
    contact:str



