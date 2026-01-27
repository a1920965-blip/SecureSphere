from typing import List
from fastapi import FastAPI,Request
from routers import users,auth
import api_services
from exception.handle import register_user_exception_handler
from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="templates")
from fastapi.staticfiles import StaticFiles
app=FastAPI()

register_user_exception_handler(app)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/')
def root(request:Request):
    context = {
        "request": request,
        "name": "Akash Gupta",
        **api_services.weather_api("Mumbai")
    }
    return templates.TemplateResponse("app.html",context)
@app.get('/test')
def test(request:Request):
    return templates.TemplateResponse("profile.html",{"request":request})
app.include_router(users.router)
app.include_router(auth.router)