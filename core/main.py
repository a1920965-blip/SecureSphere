from typing import List
from fastapi import FastAPI,Request
from core.routers import users,auth
from core import api_services,models
from core.exception.handle import register_user_exception_handler
from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="core/templates")
from fastapi.staticfiles import StaticFiles
app=FastAPI()
# models.Base.metadata.create_all(bind=engine)
register_user_exception_handler(app)

app.mount("/static", StaticFiles(directory="core/static"), name="static")

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
    return templates.TemplateResponse("app.html",{"request":request})
app.include_router(users.router)
app.include_router(auth.router)