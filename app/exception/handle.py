from fastapi import Request,status
from.custom_exceptions import VehicleNotFound,VehicleAlreadyExit,AdminAlreadyExit
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
#So this decorator registers a handler like: If any endpoint raises VehicleNotFound, run this function automatically.
templates=Jinja2Templates(directory="src/templates")
def register_user_exception_handler(app):
    @app.exception_handler(VehicleNotFound)
    def vehicle_not_found_handler(request:Request,excObj:VehicleNotFound):
        return templates.TemplateResponse("success.html",{"request":request,"status":False,"error":f"Vehicle not found:{excObj.vehicle_no}"},status_code=status.HTTP_404_NOT_FOUND)
    @app.exception_handler(VehicleAlreadyExit)
    def vehicle_allready_exit_handler(request:Request,excObj:VehicleAlreadyExit):
        return templates.TemplateResponse(
            "success.html",
            {"request": request, "error": excObj.messege,"status":False},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    @app.exception_handler(AdminAlreadyExit)
    def vehicle_allready_exit_handler(request:Request,excObj:AdminAlreadyExit):
        return templates.TemplateResponse(
            "signup.html",
            {"request": request, "error": excObj.messege,"status":False},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

