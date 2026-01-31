from fastapi import APIRouter,status,HTTPException,Request,Depends,status
from backend.core import schemas,database,models
from backend.core import utils
from backend.core.exception.custom_exceptions import Credential_Exception
from sqlalchemy.orm import Session
from backend.core.o2auth import create_Access_token,verify_token,get_current_user
import os
from fastapi.security import OAuth2PasswordRequestForm
router=APIRouter(tags=["Authentication"])

@router.post('/login',status_code=status.HTTP_202_ACCEPTED)
def validate_login(credential:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    user=db.get(models.Auth,credential.username)
    if user==None or not utils.verify(credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credential user not found!")
    token=create_Access_token({"user_id":credential.username,"role":user.role})
    return {"access_token": token,"token_type": "bearer"}
@router.post('/user/register',response_model=schemas.User_registration_response,status_code=status.HTTP_201_CREATED)
def validate_user_registration(f_data:schemas.Validate_user_registration,db:Session=Depends(database.get_db)):
    existing=db.get(models.Auth,f_data.user_id)
    if existing:
        raise Credential_Exception("User Already Exit")
    auth=models.Auth(user_id=f_data.user_id,password=utils.hash(f_data.password),role="USER")
    db.add(auth)
    Qr=utils.generate_qr_code(f_data.user_id)
    token_obj=models.Token(user_id=f_data.user_id,token=Qr["data"],token_id=Qr["token_id"])
    db.add(token_obj)
    log=models.User_logs(user_id=f_data.user_id,action="Register",name=f_data.name)
    db.add(log)
    personal=models.Personal(user_id=f_data.user_id,contact=f_data.contact,email=f_data.email,Name=f_data.name)
    db.add(personal)
    db.commit()
    return {"status":True,"message":f"{f_data.role} Register Successfully!"}
@router.post('/admin/register')
def validate_admin_registration(f_data:schemas.Validate_admin_registration,db:Session=Depends(database.get_db)):
    existing=db.get(models.Auth,f_data.user_id)
    if existing:
        raise Credential_Exception("Admin Already Exit")
    if f_data.code!="ADMINCODE":
        raise Credential_Exception("Wrong Security code!")
    else:
        auth=models.Auth(user_id=f_data.user_id,password=utils.hash(f_data.password),role="ADMIN")
        db.add(auth)
        db.commit()
    return {"status":True,"message":"Admin Register Successfully!"}
