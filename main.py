from typing import List
from fastapi import FastAPI,Request
from routers import users
import api_services
from exception.handle import register_user_exception_handler
from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="templates")

app=FastAPI()

register_user_exception_handler(app)

@app.get('/')
def root(request:Request):
    context = {
        "request": request,
        "name": "Akash Gupta",
        **api_services.weather_api("Mumbai")
    }
    return templates.TemplateResponse("app.html",context)
app.include_router(users.router)