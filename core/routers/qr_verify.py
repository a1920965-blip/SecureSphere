from fastapi import APIRouter,status,HTTPException,Request,Depends
from core import schemas,utils,database,models
from core.exception.custom_exceptions import Credential_Exception
from sqlalchemy.orm import Session
from core.o2auth import create_Access_token,verify_token,get_current_user

router=APIRouter(tags=["QrCode/Token Valdation"])

@router.get('/verify/{token}')
def token_verify(token:str,db:Session=Depends(database.get_db)):
    user=db.get(models.Token,token)
    if user==None:
        return Credential_Exception()
    return {"status":True,"message":"Verifyed user"}