from fastapi import APIRouter,status,HTTPException,Request,Depends,status
from backend.core import schemas,database,models
from backend.core import utils
from backend.core.o2auth import get_current_user
from sqlalchemy.orm import Session
from backend.core.o2auth import create_Access_token,verify_token,get_current_user
import os

router=APIRouter()

@router.get('/') # this load all request for epass, complaint or user_query, logs of user activity

def dashboard(db:Session=Depends(database.get_db),admin=Depends(get_current_user)):
    complaint=db.query(models.Complaint).all()
    epasses=db.query(models.Epass).all()
    logs=db.query(models.User_logs).all()
    return {"Compliants":[{"ticket_id":c.ticket_id,
                            "user_id":c.user_id,
                            "category":c.category,
                            "description":c.description,
                            "attachment":c.attachment,
                            "subject":c.subject} for c in complaint] if complaint else None,
            "epasses":[{"ticket_id": e.ticket_id,
            "guest_name": e.guest_name,
            "purpose": e.purpose,
            "arrival": e.arrival,
            "departure": e.departure,
            "contact": e.contact,
            "vehicle_no": e.vehicle_no,
            "status": e.status,
            "remark": e.remark} for e in epasses] if epasses else None, 
            "User_logs":[{ "user_id":l.user_id,"log_id":l.log_id,
                        "Name":l.name,"action":l.action} for l in logs] if logs else None
    }
            
