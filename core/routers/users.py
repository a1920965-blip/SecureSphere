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
def user_profile(request:Request,db:Session=Depends(database.get_db),user_id=Depends(get_current_user)):
    data=db.get(models.Auth,user_id)
    data.resident   # using lazy loading concept yaad rakhna      
    data.personal
    data.vehicle
    data.complaint
    return {"Data":data}

@router.post('/personal/')
def update_personal(user_data:schemas.Personal,user_id=Depends(get_current_user),db:Session=Depends(database.get_db)):
    user=db.get(models.Personal,user_id)
    user.contact=user_data.contact
    user.email=user_data.email
    user.designation=user_data.designation
    user.department=user_data.department
    db.commit()
    return {'status':True,"messege":"Details Updates succcesfully"}

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
    return {'status':True,"messege":"Details Updates succcesfully"}

@router.post('/vehicle/add/')
def add_vehicle(user_data:schemas.Vehicle,user_id=Depends(get_current_user),db:Session=Depends(database.get_db)):
    obj=models.Vehicle(owner=user_id,number=user_data.number)
    db.add(obj)
    db.commit()
    return {'status':True,"messege":"vehicle added succcesfully"}
@router.post('/vehicle/remove/')
def delete_vehicle(user_data:schemas.Vehicle,user_id=Depends(get_current_user),db:Session=Depends(database.get_db)):
    obj=db.get(models.Vehicle,(user_id,user_data.number))
    if obj==None:
        return {'status':False,"messege":f"vehicle does not exit of number: {user_data.number}"}
    db.delete(obj)
    db.commit()
    return {'status':True,"messege":"vehicle delete  succcesfully"}


