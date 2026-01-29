from fastapi import APIRouter,status,HTTPException,Request,Depends
from fastapi.responses import HTMLResponse,RedirectResponse
from core import schemas,utils,database,models
from sqlalchemy.orm import Session
from core.exception.custom_exceptions import InvalidCredential
from core.o2auth import create_Access_token,verify_token,get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates 

router=APIRouter(tags=["QrCode/Token Valdation"])

@router.get('/verify/{token}')
def token_verify(token:str,db:Session=Depends(database.get_db)):
    user=db.get("models.Token",token)
    if user==None:
        return InvalidCredential()
    return {"status":True,"messege":"Verifyed user"}