from fastapi import Depends,HTTPException,status,Depends
from fastapi.security import OAuth2PasswordBearer
from core import schemas
from core.exception.custom_exceptions import InvalidCredential
from datetime import datetime,timedelta
from dotenv import load_dotenv
from jose import JWTError,jwt
load_dotenv()
import os



Oauth2=OAuth2PasswordBearer(tokenUrl="login")
def create_Access_token(user_credentail:schemas.UserAuth):
    to_encode=user_credentail.copy()
    expire=datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    to_encode.update({"exp":expire})
    access_token=jwt.encode(to_encode,os.getenv("SECRET_KEY"),algorithm=os.getenv("ALGORITHM"))
    return access_token
def verify_token(token:str,credentail_exception):
    try:
        payload=jwt.decode(token,os.getenv("SECRET_KEY"),algorithms=[os.getenv("ALGORITHM")])
        return payload.get('user_id')
    except JWTError:
        raise credentail_exception()

def get_current_user(token:str=Depends(Oauth2)):
    credentail_exception=InvalidCredential
    return verify_token(token,credentail_exception)