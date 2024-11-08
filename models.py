from sqlalchemy import Boolean,Column,Integer,String,DateTime,Text
from database import Base
from sqlalchemy.sql import func

class Users(Base):
    __tablename__='users'
    
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String(50),unique=True)
    password=Column(String(200))
    email=Column(String(100))
    disabled=Column(Boolean,default=False)
    token=Column(String(200),default=None)
