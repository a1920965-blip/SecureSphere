from fastapi import APIRouter,status,HTTPException,Request,Depends
from core import schemas,utils,database,models
from sqlalchemy.orm import Session
from core.o2auth import create_Access_token,verify_token,get_current_user
router=APIRouter(tags=["Complaint"])

@router.post('/complaint')
def complaint_post(user_data: schemas.Complaint, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
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
def complaint_status(ticket_id:str,user_id=Depends(get_current_user), db: Session = Depends(database.get_db)):
    c = db.get(models.Complaint,ticket_id)
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