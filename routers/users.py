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

router=APIRouter(prefix="/user",tags=["User"])

#home page of user 
@router.get('/')
def user_home_page():
     return "This is user home page this is view after the login"

@router.get('/profile/')
def user_profile(request: Request, user_id: str):
    cursor.execute("""
        SELECT 
            p.*, r.*, v.vehicle_no, v.vehicle_type
        FROM profile p
        LEFT JOIN resident r ON r.OWNER = p.USER_ID
        LEFT JOIN vehicle v ON v.OWNER = p.USER_ID
        WHERE p.USER_ID = %s
    """, (user_id,))
    
    rows = cursor.fetchall() # Get ALL rows to capture all vehicles
    
    if not rows:
        return templates.TemplateResponse("404.html", {"request": request})

    # Initialize user data from the first row
    user_data = dict(rows[0])
    
    # Format timestamp
    if user_data.get("timestamp"):
        user_data["timestamp"] = user_data["timestamp"].isoformat()

    # Aggregate vehicles into a list
    user_data["vehicles"] = []
    for row in rows:
        if row.get("vehicle_no"): # Ensure there is actually a vehicle
            user_data["vehicles"].append({
                "vehicle_no": row["vehicle_no"],
                "vehicle_type": row["vehicle_type"]
            })

    return templates.TemplateResponse("profile.html", {"request": request, "user": user_data})#preview login page

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