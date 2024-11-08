from fastapi import FastAPI,HTTPException,Depends,status, APIRouter,Request
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine,SessionLocal,Base
from sqlalchemy.orm import Session
import os
from database import database_db
from models import Users
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jose import jwt,JWTError
from passlib.context import CryptContext
from datetime import datetime,timedelta

router=APIRouter(prefix='/users',responses={404:{'message':'No encontrado'}})

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
class UserBase(BaseModel):
    username:str
    password:str
    email:str
    
@router.post('/create_user',status_code=status.HTTP_201_CREATED)
async def create_user(user:UserBase,db:Session=Depends(get_db)):
    db_user=Users(**user.model_dump())
    db.add(db_user)
    db.commit()
    return{'message':'User successfuly created'}

@router.get('/get_user/{user_id}',status_code=status.HTTP_200_OK)
async def get_user(user_id:int,db:Session=Depends(get_db)):
    user_db=db.query(Users).filter(Users.id==user_id).first()
    return user_db

@router.put('/update_user')
async def update_user(user_id:int,user:UserBase,db:Session=Depends(get_db)):
    user_db=db.query(Users).filter(Users.id==user_id).first()
    user_db.username=user.username
    user_db.password=user.password
    user_db.email=user_db.email
    db.commit()
    return {'message':'User succesfuly updated'}

@router.delete('/delete_user/{user_id}')
async def delete_user(user_id:int,db:Session=Depends(get_db)):
    user_db=db.query(Users).filter(Users.id==user_id).first()
    db.delete(user_db)
    db.commit()
    return {'message':'User succesfuly deleted'}

@router.get('/search')
async def search(query:str,db:Session=Depends(get_db)):
    results=list(db.query(Users).filter(Users.username.ilike(f"%{query}%")))
    return results

@router.get('/get_users',status_code=status.HTTP_200_OK)
async def get_users(db:Session=Depends(get_db)):
    users=list(db.query(Users))
    return users

@router.post('/login',status_code=status.HTTP_200_OK)
async def login(user:UserBase,db:Session=Depends(get_db)):
    user_db=db.query(Users).filter(Users.username==user.username,Users.password==user.password).first()
    if user_db:
        return {'message':'Loged','user':user_db}