from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from backend.core import database,models
from .import epass,complaint
from backend.core.o2auth import verify_user

router=APIRouter(prefix="/support")
@router.get('/status/')
def tickets_status(user_id=Depends(verify_user),db:Session=Depends(database.get_db)):
    complaint=db.query(models.Complaint).filter(models.Complaint.user_id==user_id).all()
    epasses=db.query(models.Epass).filter(models.Epass.user_id==user_id).all()
    return {"success":True,
                    "data":{
                        "complaints":[{"ticket_id":c.ticket_id,
                                        "subject":c.subject,
                                        "status":c.status,
                                        "remark":c.remark,
                                        "type":"Complaint"} for c in complaint] if complaint else None,
                        "epasses":[{"ticket_id":e.ticket_id,
                                    "status":e.status,
                                    "remark":e.remark,
                                    "type":"E-pass"} for e in epasses] if epasses else None 
    }}

router.include_router(epass.router)
router.include_router(complaint.router)
