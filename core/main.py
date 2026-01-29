from fastapi import FastAPI,Request
from core.exception.handle import user_exception_handler,jwt_exception_handler,postgres_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from core.routers import auth,qr_verify
from core.routers.admin import admin
from core.routers.user import user


app=FastAPI()

origin=["*"]
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

app.include_router(qr_verify.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(admin.router)