from fastapi import APIRouter,status,HTTPException,Request,Depends
from fastapi.responses import HTMLResponse
import schemas
import utils
from database import conn,cursor
from exception.custom_exceptions import VehicleNotFound,VehicleAlreadyExit
from fastapi.templating import Jinja2Templates 
templates=Jinja2Templates(directory="templates")

router=APIRouter(prefix="/user",tags=["User"])

#home page of user 
@router.get('/')
def user_home_page():
     return "This is user home page this is view after the login"

#preview login page
@router.get('/login')
def user_login(request:Request):
    return templates.TemplateResponse("auth.html",{"request":request,"status":False})

@router.post('/login')
def validate_login(request:Request,credential:dict):
    print(type(credential))
    cursor.execute("SELECT * FROM AUTH WHERE USER_ID=%s ",(credential["user_id"],))
    print("data fetched from database")
    data=cursor.fetchone()
    print("data type of coming from database: ",type(data))
    if data==None or credential["password"]!=data['password']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="!Invalid Credential")
    return {"status":True,"messege":"login successfully"}

@router.get('/register')
def user_register(request:Request):
    return templates.TemplateResponse("auth.html",{"request":request,"status":True})

@router.post('/register')
def validate_user_registration(request:Request,credentail:dict):
    cursor.execute("INSERT INTO AUTH (USER_ID,PASSWORD,CONTACT,EMAIL) VALUES (%s,%s,%s,%s)RETURNING*;",(credentail["user_id"],credentail["password"],credentail["contact"],credentail["email"]))
    data=cursor.fetchone()
    conn.commit()
    return{"status":True,"messege":"Registratiion Done","Data":data}
    


     
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