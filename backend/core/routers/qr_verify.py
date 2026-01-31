from fastapi import APIRouter,status,HTTPException,Request,Depends
from backend.core import schemas,utils,database,models
from backend.core.exception.custom_exceptions import Credential_Exception
from sqlalchemy.orm import Session
from backend.core.o2auth import create_Access_token,verify_token,get_current_user

router=APIRouter(tags=["QrCode/Token Valdation"])

@router.get('/verify/')
def token_verify(token_id:str,db:Session=Depends(database.get_db)):
    user=db.query(models.Token).filter(models.Token.token_id==token_id)
    if user==None:
        raise Credential_Exception("Invalid Token")
    return {"status":True,"message":"Verifyed user"}