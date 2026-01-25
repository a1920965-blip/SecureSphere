from typing import List
from fastapi import FastAPI,Request
from routers import users
from exception.handle import register_user_exception_handler
from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="templates")

app=FastAPI()

register_user_exception_handler(app)

@app.get('/')
def root(request:Request):
    return templates.TemplateResponse("app.html",{"request":request})
app.include_router(users.router)