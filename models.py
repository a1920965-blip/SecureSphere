from sqlalchemy import Column,Integer,String,TIMESTAMP,text
from sqlalchemy.ext.declarative import declarative_base
base=declarative_base()

class User(base):
    __tablename__="user"
    id=Column(Integer,index=True)
    name=Column(String,nullable=False)
    vehicle_no=Column(String,nullable=False,unique=True,primary_key=True)
    purpose=Column(String,default="")
    timestamp=Column(TIMESTAMP,server_default=text("now()"),nullable=False)
    status=Column(String,default="Pending",nullable=False)
    remark=Column(String,default="")



