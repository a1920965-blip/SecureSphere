from fastapi import APIRouter,status,HTTPException,Request,Depends,status
from backend.core import schemas,database,models
from backend.core import utils
from backend.core.exception.custom_exceptions import Content_Not_Found
from backend.core.o2auth import verfiy_admin
from sqlalchemy.orm import Session
import os

router=APIRouter()

@router.get('/') # this load all request for epass, complaint or user_query, logs of user activity

def dashboard(db:Session=Depends(database.get_db),admin=Depends(verfiy_admin)):
    complaint=db.query(models.Complaint).all()
    epasses=db.query(models.Epass).all()
    logs=db.query(models.User_logs).all()
    return {"Compliants":[{"ticket_id":c.ticket_id,
                            "user_id":c.user_id,
                            "category":c.category,
                            "description":c.description,
                            "attachment":c.attachment,
                            "subject":c.subject,
                            "status":c.status,
                            "remark":c.remark} for c in complaint] if complaint else None,
            "epasses":[{"ticket_id": e.ticket_id,
            "guest_name": e.guest_name,
            "purpose": e.purpose,
            "arrival": e.arrival,
            "departure": e.departure,
            "contact": e.contact,
            "vehicle_no": e.vehicle_no,
            "status": e.status,
            "remark": e.remark} for e in epasses] if epasses else None, 
            "User_logs":[{ "user_id":l.user_id,"log_id":l.logs_id,
                        "Name":l.name,"action":l.action} for l in logs] if logs else None
    }
@router.put('/complaint/action',status_code=status.HTTP_204_NO_CONTENT)
def update_complaint(ticket_id:int,c_Data:schemas.Complaint_update,admin=Depends(verfiy_admin),db:Session=Depends(database.get_db)):
    comp=db.get(models.Complaint,ticket_id)
    if comp==None:
        raise Content_Not_Found("Invalid Request")
    elif comp.status.upper()=="APPROVED":
        return "Already Aprroved"
    elif comp.status.upper()=="PENDING":
        comp.status=c_Data.status
        comp.remark=c_Data.remark
        db.commit()
    else:
        raise Content_Not_Found("Invalid Request")

@router.put('/epass/action',status_code=status.HTTP_204_NO_CONTENT)
def update_epasses(ticket_id:str,e_data:schemas.Epass_update,admin=Depends(verfiy_admin),db:Session=Depends(database.get_db)):
    epass=db.get(models.Epass,ticket_id)
    if epass==None or epass.status.upper()!="PENDING":
        raise Content_Not_Found("Invalid Request")
    epass.status=e_data.status
    epass.remark= e_data.remark
    token_obj=None
    if e_data.status=="APPROVED":  #  guestid function is remaning we can also import it into utils 
        guest_id=epass.guest_name.strip().lower()
        Qr=utils.generate_qr_code(guest_id)
        token_obj=models.Token(user_id=guest_id,token=Qr["data"],token_id=Qr["token_id"])
        db.add(token_obj)
        db.commit()
        db.refresh(token_obj)
    db.commit()


    
