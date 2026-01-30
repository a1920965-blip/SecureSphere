from fastapi import FastAPI,Request
from backend.core.exception.handle import user_exception_handler,jwt_exception_handler,postgres_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from backend.core.routers import auth,qr_verify
from backend.core.routers.admin import admin
from backend.core.routers.user import user
import os
from dotenv import load_dotenv
load_dotenv()
app=FastAPI()

BASE_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FRONTEND_DIR=os.path.join(BASE_DIR,"frontend/static")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user_exception_handler(app)
jwt_exception_handler(app)
postgres_exception_handler(app)

@app.get('/')
def root(request:Request):
    return "root directory"
app.include_router(qr_verify.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(admin.router)