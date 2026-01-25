class VehicleNotFound(Exception):
    def __init__(self,vehicle_no):
        self.vehicle_no=vehicle_no
class InvalidCredential(Exception):
    messege="Invalid Credential "
class AdminAlreadyExit(Exception):
    messege="You Already Have an Account"
    