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
def update_complaint(ticket_id:int,c_Data:schemas.Complaint_update,admin=Depends(get_current_user),db:Session=Depends(database.get_db)):
    comp=db.get(models.Complaint,ticket_id)
    if comp==None:
        return "Invlaid Token"
    elif comp.status.upper()=="APPROVED":
        return "Already Aprroved"
    elif comp.status.upper()=="PENDING":
        # comp.user_id=c_Data.user_id
        # comp.category=c_Data.category
        # comp.description=c_Data.description
        # comp.subject=c_Data.subject
        # comp.attachment=c_Data.attachment
        comp.status=c_Data.status
        comp.remark=c_Data.remark
        db.commit()
        return {"status":True}
    else:
        return {"status":False,"mesage":"Invalid Request"}
@router.put('/epass/action')
def update_epasses(ticket_id:str,e_data:schemas.Epass_update,admin=Depends(get_current_user),db:Session=Depends(database.get_db)):
    epass=db.get(models.Epass,ticket_id)
    if epass==None:
        return "Invlaid Token"
    elif epass.status.upper()=="APPROVED":
        return "Already Aprroved"
    elif epass.status.upper()=="PENDING":
        # epass.guest_name=e_data.guest_name
        # epass.purpose= e_data.purpose
        # epass.arrival= e_data.arrival
        # epass.departure= e_data.departure
        # epass.contact= e_data.contact
        # epass.vehicle_no= e_data.vehicle_no
        epass.status=e_data.status
        epass.remark= e_data.remark
        t=None
        if e_data.status=="APPROVED":  #  guestid function is remaning we can also import it into utils 
            guest_id=epass.guest_name.strip().lower()
            Qr=utils.generate_qr_code(guest_id)
            t=models.Token(user_id=guest_id,token=Qr["data"],token_id=Qr["token_id"])
            db.add(t)
            db.commit()
            db.refresh(t)
            return {"status":True,"data":t}
        db.commit()
        return {"status":True,"Data":None}
    else:
        return {"status":False,"mesage":"Invalid Request"}



    
