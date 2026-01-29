from typing import List
from fastapi import FastAPI,Request
from core.routers import users,auth,complaint,epass
from core import api_services,models
from core.exception.handle import register_user_exception_handler
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

origin=["10.10.3.178"]
app.middleware.cors(
    CORSMiddleware,
    allow_origin=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


register_user_exception_handler(app)
@app.get('/')
def root(request:Request):
    return "This is my home page"

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(complaint.router)
app.include_router(epass.router)