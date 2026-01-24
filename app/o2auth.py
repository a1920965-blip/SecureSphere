from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from .import schemas
from datetime import datetime,timedelta
from dotenv import load_dotenv
from jose import JWTError,jwt
load_dotenv()

SECRET_KEY='b2b5fdc19c2726c1a0cc533e66a5db26a4b726f0a108a95b326776623450e888'
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=120


Oauth2=OAuth2PasswordBearer(toeknUrl="login")
def create_Access_token(user_credentail:schemas.user_credential):
    to_encode=user_credentail.copy()
    expire=datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire})
    access_token=jwt.encode(to_encode,SECRET_KEY,algortitm=ALGORITHM)
    return access_token
def verify_token(token:str,credentail_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload.get('user_name')
    except JWTError:
        raise credentail_exception

