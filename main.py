from fastapi import FastAPI
from database import engine,SessionLocal,Base
from fastapi.middleware.cors import CORSMiddleware
from routers import users

origins = [
    "http://localhost:3000", 
]

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(users.router)

Base.metadata.create_all(bind=engine)
