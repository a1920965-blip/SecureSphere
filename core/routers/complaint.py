from fastapi import APIRouter,status,HTTPException,Request,Depends
from core import schemas,utils,database,models
from sqlalchemy.orm import Session
from core.o2auth import create_Access_token,verify_token,get_current_user
router=APIRouter(tags=["Complaint"])

@router.post('/user/complaint')
def submit_complaint(user_data: schemas.Complaint, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
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
        "messege": "Complaint submitted successfully!",
        "complaint_id": obj.complaint_id
    }
@router.get('/user/complaint')
def complaint_status(user_id=Depends(get_current_user), db: Session = Depends(database.get_db)):
    complaints = db.query(models.Complaint).filter(models.Complaint.user_id == user_id).all()
    return {
        "status": True, 
        "data": [{
            "complaint_id": c.complaint_id,
            "category": c.category,
            "subject": c.subject,
            "description": c.description,
            "status": c.action or "Pending",
            "attachment": c.attachment
        } for c in complaints]
    }