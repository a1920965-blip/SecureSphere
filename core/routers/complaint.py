from fastapi import APIRouter,status,HTTPException,Request,Depends
from core import schemas,utils,database,models
from sqlalchemy.orm import Session
from core.o2auth import create_Access_token,verify_token,get_current_user
router=APIRouter(tags=["Complaint"])

@router.post('/user/complaint')
def submit_complaiant(user_data:schemas.Complaint,db:Session=Depends(database.get_db),user=Depends(get_current_user)):
    obj=models.Complaint(user_id=user,category=user_data.category,description=user_data.description,attachement=user_data.attachement,subject=user_data.subject)
    db.add(obj)
    db.commit()
    return {"status":True,"messege":"Complaint submit succesfully!","data":obj}

@router.get('user/complaint')
def complaint_status(user_id=Depends(get_current_user),db:Session=Depends(database.get_db)):
    data=db.query(models.Complaint).filter(models.Complaint.user_id==user_id).all()
    return {"status":True,"data":data}