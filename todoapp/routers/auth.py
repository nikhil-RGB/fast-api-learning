from typing import Annotated
from starlette import status
from database import SessionLocal
from fastapi import Depends, FastAPI, APIRouter
from pydantic import BaseModel
from sqlalchemy import Boolean
from passlib.context import CryptContext
from models import Users
from fastapi.security import OAuth2PasswordRequestForm
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

#Attempt to authenticate the user.
def authenticate_user(username:str,password:str,db):
    user=db.query(Users).filter(Users.username==username).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password,user.hashed_password):
        return False
    return True


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

@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    user=authenticate_user(form_data.username,form_data.password,db)
    if user:
        return "User Authenticated"
    else:
        return "Authentication Failed"
    
    