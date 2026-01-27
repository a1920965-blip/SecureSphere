from sqlalchemy import Column,Integer,String,TIMESTAMP,text
from sqlalchemy.ext.declarative import declarative_base
base=declarative_base()

# class Auth(base):
#     __tablename__="user"
#     id=Column(Integer,index=True)
#     email=Column(String,nullable=False)
#     user_name=Column(String,nullable=False,unique=True,primary_key=True)
#     password=Column(String,nullable=False)

# class address(base):
#   __tablename__="address"
    # house_no=Column(String,nullable=False)
    # apratment_name=Column(String)
    # street=Column(string)
    # city=COlumn(String)
    # pincode=Column(String)
    
# class Profile(base):
#     __tablename__="profile"
#     Name=Column(String,nullable=False)
#     dept=Column(String)
#     contact=Column(String,default="")
#     address=Column(String)
#     timestamp=Column(TIMESTAMP,server_default=text("now()"),nullable=False)








