from fastapi import APIRouter,status,HTTPException,Request,Depends,status
from fastapi.responses import HTMLResponse,RedirectResponse
from core import schemas,database,models
from core.exception.custom_exceptions import InvalidCredential
from core import utils
from sqlalchemy.orm import Session
from core.o2auth import create_Access_token,verify_token,get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates 
templates=Jinja2Templates(directory="templates")

router=APIRouter(tags=["User"])

@router.get('/login')
def user_login(request:Request):
    return templates.TemplateResponse("auth.html",{"request":request,"status":False})

@router.post('/login')
def validate_login(db:Session=Depends(database.get_db),credential:OAuth2PasswordRequestForm=Depends()):
    user=db.get(models.Auth,credential.username)
    print("yaha tak sahi hai:",user)
    if user==None or not utils.verify(credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="INvalid Credential!")
    token=create_Access_token({"user_id":credential.username,"password":credential.password})
    return {"status":True,"token":token}

@router.get('/register')
def user_register(request:Request):
    return templates.TemplateResponse("auth.html",{"request":request,"status":True})

@router.post('/register')
def validate_user_registration(X:schemas.NewUser,db:Session=Depends(database.get_db)):
    auth=models.Auth(user_id=X.user_id,password=utils.hash(X.password))
    db.add(auth)
    profile=models.Profile(user_id=X.user_id,contact=X.contact,email=X.email,Name=X.name)
    db.add(profile)
    db.commit()
    return {"status":True,"messenge":"User Register Successfully!"}

    # def validate_login(request:Request,credential:OAuth2PasswordRequestForm=Depends()):

    # cursor.execute("SELECT * FROM AUTH WHERE USER_ID=%s ",(credential.username,))
    # data=cursor.fetchone()
    # if data==None or not utils.verify(credential.password,data['password']):
    #     raise InvalidCredential()
    # token=create_Access_token({"user_id":credential.username,"id":data['id']})

    # response=RedirectResponse(url="/",status_code=303)
    # response.set_cookie(key="token",value=token,expires=120)
    # return response
