from fastapi import APIRouter,status,HTTPException,Request,Depends
from fastapi.responses import HTMLResponse,RedirectResponse
import schemas
from exception.custom_exceptions import InvalidCredential
import utils
from fastapi.security import OAuth2PasswordRequestForm
from database import conn,cursor
from fastapi.templating import Jinja2Templates 
templates=Jinja2Templates(directory="templates")

router=APIRouter(prefix="/user",tags=["User"])

#home page of user 
@router.get('/')
def user_home_page():
     return "This is user home page this is view after the login"

@router.get('/profile')
def user_profile(user_id:str):
cursor.execute("""
    SELECT 
        p.*,
        r.*,
        v.*
    FROM PROFILE p
    LEFT JOIN resident r ON r.OWNER = p.USER_ID
    LEFT JOIN vehicle v ON v.OWNER = p.USER_ID
    WHERE p.USER_ID = %s
""", (user_id,))

result = cursor.fetchone()

    return {"status":True,"data":result}
#preview login page
@router.get('/login')
def user_login(request:Request):
    return templates.TemplateResponse("auth.html",{"request":request,"status":False})

@router.post('/login')
def validate_login(request:Request,credential:schemas.UserAuth=Depends(schemas.UserAuth.as_form)):
    cursor.execute("SELECT * FROM AUTH WHERE USER_ID=%s ",(credential.user_id,))
    data=cursor.fetchone()
    if data==None or not utils.verify(credential.password,data['password']):
        raise InvalidCredential()
    return RedirectResponse(url="/",status_code=303)

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
        RETURNING USER_ID,;
        """,
        (
            credential.user_id,
            utils.hash(credential.password),
            credential.email,
        ),
    )
    cursor.execute(
        """
        INSERT INTO PROFILE (NAME,CONTACT)
        VALUES (%s, %s, %s)
        RETURNING ;
        """,
        (
            credential.name,
            credential.contact,
            credential.email
        ),
    )

    user = cursor.fetchone()
    conn.commit()

    return RedirectResponse(
        url="/user/login",
        status_code=status.HTTP_303_SEE_OTHER
    )
# @router.post('/user/register/',response_class=HTMLResponse,status_code=status.HTTP_201_CREATED)
# def user_register(request:Request,user_Data:schemas.Register_vehicle=Depends(schemas.Register_vehicle.as_form)):
#     details=None
#     try:
#         cursor.execute("""INSERT INTO vehicle_record(name,purpose,vehicle_no,remark) VALUES (%s,%s,%s,%s)RETURNING* """,(user_Data.name.upper(),user_Data.purpose,user_Data.vehicle_no.upper(),user_Data.remark))
#         details=cursor.fetchone()
#         print(type(details))
#         conn.commit()
#         return templates.TemplateResponse(
#         "success.html",
#         {"request": request, "details": details,"status":True}
#         )
#     except Exception as error:
#         conn.rollback()
#         raise VehicleAlreadyExit()
    
# @router.get('/status/')
# def check_status(request:Request):
#     return templates.TemplateResponse("status.html",{"request":request})

# @router.get('/vehicle/',response_class=HTMLResponse)
# def get_detail(request:Request,vehicle_no:str):
#         cursor.execute("""SELECT * FROM vehicle_record WHERE "vehicle_no"=%s """,(vehicle_no,))
#         details=cursor.fetchone()
#         if details==None:
#             raise VehicleNotFound(vehicle_no)
#         return templates.TemplateResponse(
#         "success.html",
#         {"request": request, "details": details,"status":True}
#         )