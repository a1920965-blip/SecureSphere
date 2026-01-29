from fastapi import APIRouter,status,HTTPException,Request,Depends
from core import schemas,utils,database,models
from sqlalchemy.orm import Session
from core.o2auth import create_Access_token,verify_token,get_current_user
router=APIRouter(prefix="/user",tags=["User"])

#home page of user 
@router.get('/')
def user_home_page():
     return "This is user home page this is view after the login"

@router.get('/profile/')
def user_profile(db: Session = Depends(database.get_db), user_id=Depends(get_current_user)):
    auth_user = db.get(models.Auth, user_id)
    if not auth_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Load relationships
    personal = auth_user.personal[0] if auth_user.personal else None
    resident = auth_user.resident[0] if auth_user.resident else None
    vehicles = auth_user.vehicle
    complaints = auth_user.complaint
    
    return {
        "status": True,
        "data": {
            "user_id": auth_user.user_id,
            "name": personal.Name if personal else None,
            "email": personal.email if personal else None,
            "contact": personal.contact if personal else None,
            "department": personal.department if personal else None,
            "designation": personal.designation if personal else None,
            "timestamp": personal.timestamp.isoformat() if personal else None,
            "house_no": resident.house_no if resident else None,
            "block": resident.block if resident else None,
            "city": resident.city if resident else None,
            "state": resident.state if resident else None,
            "pincode": resident.pincode if resident else None,
            "vehicles": [{"number": v.number} for v in vehicles],
            "complaints": [{
                "complaint_id": c.complaint_id, 
                "category": c.category,
                "subject": c.subject,
                "status": c.action or "Pending"
            } for c in complaints]
        }
    }

@router.post('/personal/')
def update_personal(user_data:schemas.Personal,user_id=Depends(get_current_user),db:Session=Depends(database.get_db)):
    user=db.get(models.Personal,user_id)
    user.contact=user_data.contact
    user.email=user_data.email
    user.designation=user_data.designation
    user.department=user_data.department
    db.commit()
    return {'status':True,"message":"Details Updates succesfully"}

@router.post('/resident/')
def update_resident(user_data:schemas.Resident,user_id=Depends(get_current_user),db:Session=Depends(database.get_db)):
    
    user=db.get(models.Resident,user_id)
    if user is None:
        obj=models.Resident(owner=user_id,house_no=user_data.house_no,block=user_data.block,city=user_data.city,state=user_data.state,pincode=user_data.pincode)
        db.add(obj)
    else:
        user.house_no=user_data.house_no
        user.block=user_data.block
        user.city=user_data.city
        user.state=user_data.state
        user.pincode=user_data.pincode
    db.commit()
    return {'status':True,"message":"Details Updates succesfully"}

@router.post('/vehicle/add/')
def add_vehicle(user_data:schemas.Vehicle,user_id=Depends(get_current_user),db:Session=Depends(database.get_db)):
    obj=models.Vehicle(owner=user_id,number=user_data.number)
    db.add(obj)
    db.commit()
    return {'status':True,"message":"vehicle added succesfully"}
@router.post('/vehicle/remove/')
def delete_vehicle(user_data:schemas.Vehicle,user_id=Depends(get_current_user),db:Session=Depends(database.get_db)):
    obj=db.get(models.Vehicle,(user_id,user_data.number))
    if obj==None:
        return {'status':False,"message":f"vehicle does not exit of number: {user_data.number}"}
    db.delete(obj)
    db.commit()
    return {'status':True,"message":"vehicle delete  succesfully"}


