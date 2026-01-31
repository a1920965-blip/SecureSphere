from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from backend.core.o2auth import verfiy_admin
from backend.core import database,models
router=APIRouter()
@router.get('/users')
def list_users(admin=Depends(verfiy_admin),db:Session=Depends(database.get_db)):
    users=db.query(models.Personal.user_id,models.Personal.Name).all()
    return {"status":True,"users":[{"user_id":u.user_id,"Name":u.Name} for u in users] if users else None}
@router.get('/user/')
def user_profile(user_id:str,db:Session=Depends(database.get_db),admin=Depends(verfiy_admin)):
    user=db.get(models.Auth,user_id)
    personal= user.personal[0] if user.personal else None
    resident= user.resident[0] if user.resident else None
    vehicle= user.vehicle
    return {"status":True,
                "data":{"user_id":user.user_id,
                        "Name":personal.Name,
                        "designation": personal.designation if personal.designation else None,
                        "department":personal.department if personal.department else None,
                        "contact":personal.contact,
                        "email":personal.email,
                        "house_no": resident.house_no if resident else None,                                
                        "block": resident.block if resident else None,                                
                        "city": resident.city if resident else None,                                
                        "state": resident.state if resident else None,                                
                        "pincode": resident.pincode if resident else None,
                        "vehicles":[{"Number":v.number} for v in vehicle] if vehicle else None
                }
                }   
                               