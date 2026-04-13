from typing import Annotated
from starlette import status
from database import SessionLocal
from fastapi import Depends, FastAPI, APIRouter
from pydantic import BaseModel
from sqlalchemy import Boolean
from passlib.context import CryptContext
from models import Users
from routers.todos import get_db,Session
router=APIRouter()
bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
class UserRequest(BaseModel):
    email:str
    username:str
    first_name:str
    last_name:str
    password:str
    role: str

    def get_db():
        db= SessionLocal()
        try:
            yield db
        finally:
            db.close()

db_dependency=Annotated[Session,Depends(get_db)]

@router.get("/auth/")
async def  get_user():
    return {'user':'authenticated'}

@router.post("/auth/create_user",status_code=status.HTTP_201_CREATED)
async def create_user(user_request:UserRequest,db:db_dependency):
     create_user_model=Users(
         email=user_request.email,
         username=user_request.username,
         first_name=user_request.first_name,
         last_name=user_request.last_name,
         hashed_password= bcrypt_context.hash(user_request.password),
         is_active=True,
         role=user_request.role
     )
     db.add(create_user_model)
     db.commit()
     return create_user_model    