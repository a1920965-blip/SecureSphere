from fastapi import APIRouter,status,HTTPException,Request,Depends
from backend.core import schemas,utils,database,models
from sqlalchemy.orm import Session
from backend.core.o2auth import verify_token,verify_user
from backend.core.exception.custom_exceptions import Content_Not_Found
from sqlalchemy import and_
router=APIRouter(tags=["Complaint"])

@router.post('/complaint')
def complaint_post(user_data: schemas.Complaint_post, db: Session = Depends(database.get_db), user=Depends(verify_user)):
    obj = models.Complaint(
        user_id=user,
        category=user_data.category,
        description=user_data.description,
        attachment=user_data.attachment,
        subject=user_data.subject
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)  # Get the auto-generated complaint_id
    
    return {
        "status": True, 
        "message": "Complaint submitted successfully!",
        "ticket_id": obj.ticket_id
    }
@router.get('/complaint')
def complaint_status(ticket_id:int,user_id=Depends(verify_user), db: Session = Depends(database.get_db)):
    c= db.query(models.Complaint).filter(and_(models.Complaint.ticket_id == ticket_id,models.Complaint.user_id==user_id)).first()
    if c is None:
        raise Content_Not_Found("Complaint not found or you don't have access to it")
    return {
        "status": True, 
        "data": {
            "ticket_id": c.ticket_id,
            "category": c.category,
            "subject": c.subject,
            "description": c.description,
            "status": c.status or "Pending",
            "attachment": c.attachment
        }
    }