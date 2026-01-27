from fastapi import APIRouter,status,HTTPException,Request,Depends
from fastapi.responses import HTMLResponse,RedirectResponse
import schemas
from exception.custom_exceptions import InvalidCredential
import utils
from o2auth import create_Access_token,verify_token,get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from database import conn,cursor
from fastapi.templating import Jinja2Templates 
templates=Jinja2Templates(directory="templates")

router=APIRouter(tags=["User"])

@router.get('/login')
def user_login(request:Request):
    return templates.TemplateResponse("auth.html",{"request":request,"status":False})

@router.post('/login')
def validate_login(request:Request,credential:OAuth2PasswordRequestForm=Depends()):

    cursor.execute("SELECT * FROM AUTH WHERE USER_ID=%s ",(credential.username,))
    data=cursor.fetchone()
    if data==None or not utils.verify(credential.password,data['password']):
        raise InvalidCredential()
    token=create_Access_token({"user_id":credential.username,"id":data['id']})

    response=RedirectResponse(url="/",status_code=303)
    response.set_cookie(key="token",value=token,expires=120)
    return response

@router.get('/register')
def user_register(request:Request):
    return templates.TemplateResponse("auth.html",{"request":request,"status":True})

@router.post('/register')
def validate_user_registration(
    request: Request,
    credential: schemas.NewUser = Depends(schemas.NewUser.as_form),
):
    cursor.execute(
        """
        INSERT INTO AUTH (USER_ID, PASSWORD)
        VALUES (%s, %s)
        RETURNING USER_ID;
        """,
        (
            credential.user_id,
            utils.hash(credential.password),
        ),
    )
    cursor.execute(
        """
        INSERT INTO PROFILE (NAME,CONTACT,EMAIL,USER_ID)
        VALUES (%s, %s, %s, %s);
        """,
        (
            credential.name,
            credential.contact,
            credential.email,
            credential.user_id
        ),
    )
    conn.commit()
    return RedirectResponse(
        url="/user/login",
        status_code=status.HTTP_303_SEE_OTHER
    )