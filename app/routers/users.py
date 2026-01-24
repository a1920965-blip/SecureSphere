from fastapi import APIRouter,status,HTTPException,Request,Depends
from fastapi.responses import HTMLResponse
from .. import schemas
from ..database import conn,cursor
from ..exception.custom_exceptions import VehicleNotFound,VehicleAlreadyExit
from fastapi.templating import Jinja2Templates 
templates=Jinja2Templates(directory="src/templates")

router=APIRouter(prefix="/user",tags=["User"])
#home page of user 
@router.get('/')
def user_home_page(request:Request):
     return "This is user home page this is view after the login"

@router.get('/login')
def user_login():
    pass

@router.post('/login')
def validate_login(credential:dict):
    pass

@router.get('/register')
def user_register():
     pass

@router.post('/register')
def validate_user_registration(credential:dict):
     pass

     

     


@router.post('/user/register/',response_class=HTMLResponse,status_code=status.HTTP_201_CREATED)
def user_register(request:Request,user_Data:schemas.Register_vehicle=Depends(schemas.Register_vehicle.as_form)):
    details=None
    try:
        cursor.execute("""INSERT INTO vehicle_record(name,purpose,vehicle_no,remark) VALUES (%s,%s,%s,%s)RETURNING* """,(user_Data.name.upper(),user_Data.purpose,user_Data.vehicle_no.upper(),user_Data.remark))
        details=cursor.fetchone()
        print(type(details))
        conn.commit()
        return templates.TemplateResponse(
        "success.html",
        {"request": request, "details": details,"status":True}
        )
    except Exception as error:
        conn.rollback()
        raise VehicleAlreadyExit()
    
@router.get('/status/')
def check_status(request:Request):
    return templates.TemplateResponse("status.html",{"request":request})

@router.get('/vehicle/',response_class=HTMLResponse)
def get_detail(request:Request,vehicle_no:str):
        cursor.execute("""SELECT * FROM vehicle_record WHERE "vehicle_no"=%s """,(vehicle_no,))
        details=cursor.fetchone()
        if details==None:
            raise VehicleNotFound(vehicle_no)
        return templates.TemplateResponse(
        "success.html",
        {"request": request, "details": details,"status":True}
        )