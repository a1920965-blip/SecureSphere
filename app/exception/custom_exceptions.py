class VehicleNotFound(Exception):
    def __init__(self,vehicle_no):
        self.vehicle_no=vehicle_no
class VehicleAlreadyExit(Exception):
    messege="Already Appplied for Registration"
class AdminAlreadyExit(Exception):
    messege="You Already Have an Account"
    