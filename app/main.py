from typing import List
from fastapi import FastAPI
from .routers import users
from .exception.handle import register_user_exception_handler


app=FastAPI()

register_user_exception_handler(app)

@app.get('/')
def root():
    return "This is my home page"
app.include_router(users.router)