from fastapi import APIRouter,status,HTTPException,Request,Depends
from backend.core import schemas,utils,database,models
from backend.core.exception.custom_exceptions import Credential_Exception
from sqlalchemy.orm import Session

router=APIRouter(tags=["QrCode/Token Valdation"])

@router.get('/verify/')
def token_verify(token_id:str,db:Session=Depends(database.get_db)):
    user=db.query(models.Token).filter(models.Token.token_id==token_id).first()
    if user==None:
        raise Credential_Exception("Invalid Token")
    return {"success":True,"message":"Verifyed user"}