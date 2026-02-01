from fastapi import APIRouter,status,HTTPException,Request,Depends
from backend.core import schemas,utils,database,models
from backend.core.exception.custom_exceptions import Content_Not_Found
from sqlalchemy.orm import Session
from backend.core.o2auth import verify_user
from sqlalchemy import and_
router=APIRouter(tags=["E-Pass"])

@router.post('/epass')
def Epass_post(user_data:schemas.Epass_post,user_id=Depends(verify_user),db:Session=Depends(database.get_db)):
    obj=models.Epass(user_id=user_id,vehicle_no=user_data.vehicle_no,
                    contact=user_data.contact,guest_name=user_data.guest_name,
                    purpose=user_data.purpose,arrival=user_data.arrival,
                    departure=user_data.departure)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {"success":True,"message":"Request Submited","ticket_id":obj.ticket_id}
@router.get('/epass')
def Epass_get(ticket_id:int,user_id=Depends(verify_user), db: Session = Depends(database.get_db)):
    e = db.query(models.Epass).filter(and_(models.Epass.ticket_id == ticket_id,models.Epass.user_id==user_id)).first()
    print(user_id)
    if e==None:
        raise Content_Not_Found("Invalid Ticket Id")
    data={
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
    if e.status.upper()=="APPROVED":
        guest_id=e.guest_name.strip().lower()
        t=db.query(models.Token).filter(models.Token.user_id==guest_id).first()
        data.update({"qr_data":t.token_id})
    return {"success": True,"data": data}