from typing import List
from fastapi import FastAPI,Request
from core.routers import users,auth,complaint,epass,qr
from core import api_services,models
from core.exception.handle import user_exception_handler,jwt_exception_handler,postgres_exception_handler
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

origin=["10.10.3.178"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user_exception_handler(app)
jwt_exception_handler(app)
postgres_exception_handler(app)

@app.get('/')
def root(request:Request):
    return "This is my root page"

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(complaint.router)
app.include_router(epass.router)
app.include_router(qr.router)