from fastapi import APIRouter,status,HTTPException,Request,Depends,status
from core import schemas,database,models
from core import utils
from sqlalchemy.orm import Session
from core.o2auth import create_Access_token,verify_token,get_current_user
import os

router=APIRouter(tags=["Authentication"])

@router.get('/login')
def user_login(request:Request):
    pass

@router.post('/login')
def validate_login(credential:schemas.UserAuth,db:Session=Depends(database.get_db)):
    user=db.get(models.Auth,credential.user_id)
    if user==None or not utils.verify(credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="INvalid Credential!")
    token=create_Access_token({"user_id":credential.user_id})
    return {"status":True,"token":token, "user_id": credential.user_id}

@router.get('/register')
def user_register(request:Request):
    pass
@router.post('/register')
def validate_user_registration(user_data:schemas.NewUser,db:Session=Depends(database.get_db)):
    auth=models.Auth(user_id=user_data.user_id,password=utils.hash(user_data.password))
    db.add(auth)

    Qr=utils.generate_qr_code(user_data.user_id)
    token_obj=models.Token(user_id=user_data.user_id,token=Qr["data"],token_id=Qr["token_id"])
    db.add(token_obj)

    personal=models.Personal(user_id=user_data.user_id,contact=user_data.contact,email=user_data.email,Name=user_data.name)
    db.add(personal)
    db.commit()
    return {"status":True,"messege":"User Register Successfully!"}


