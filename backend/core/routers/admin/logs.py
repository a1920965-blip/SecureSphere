from fastapi import APIRouter,status,HTTPException,Request,Depends,status
from backend.core import schemas,database,models
from backend.core import utils
from backend.core.exception.custom_exceptions import Content_Not_Found
from backend.core.oauth2 import verify_admin
from sqlalchemy.orm import Session
import os

router=APIRouter()

@router.get('/users/logs')
def user_logs(db:Session=Depends(database.get_db),admin=Depends(verify_admin)):
    logs=db.query(models.User_logs).all()
    data = [{ 
        "user_id": l.user_id,
        "log_id": l.logs_id,
        "Name": l.name,
        "action": l.action
    } for l in logs] if logs else None
    return {"success":True,"data":data} 