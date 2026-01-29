from fastapi import APIRouter,status,HTTPException,Request,Depends
from core import schemas,utils,database,models
from sqlalchemy.orm import Session
from core.o2auth import create_Access_token,verify_token,get_current_user
router=APIRouter(tags=["E-Pass"])

@router.post('/epass')
def Epass_post(user_data:schemas.Epass,user_id=Depends(get_current_user),db:Session=Depends(database.get_db)):
    obj=models.Epass(user_id=user_id,vehicle_no=user_data.vehicle_no,
                    contact=user_data.contact,guest_name=user_data.name,
                    purpose=user_data.purpose,arrival=user_data.arrival,
                    departure=user_data.departure)
    db.add(obj)
    db.commit()
    return {"status":True,"message":"Request Submited"}
@router.get('/epass')
def Epass_get(ticket_id:int,user_id=Depends(get_current_user), db: Session = Depends(database.get_db)):
    e = db.query(models.Epass).filter(models.Epass.ticket_id == ticket_id).first()
    return {
        "status": True,
        "data": {
            "ticket_id": e.ticket_id,
            "guest_name": e.guest_name,
            "purpose": e.purpose,
            "arrival": e.arrival,
            "departure": e.departure,
            "contact": e.contact,
            "vehicle_no": e.vehicle_no,
            "status": e.status,
            "remark": e.remark
        }
    }