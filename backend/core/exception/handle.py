from fastapi import Request,status
from .custom_exceptions import Credential_Exception
from fastapi.responses import JSONResponse
#So this decorator registers a handler like: If any endpoint raises VehicleNotFound, run this function automatically.
def user_exception_handler(app):

    @app.exception_handler(Credential_Exception)
    def credential_handler(exec:Credential_Exception):
        return {"status":False,"message":Credential_Exception.msg}


def jwt_exception_handler(app):
    pass



def postgres_exception_handler(app):
    pass 
