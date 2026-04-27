from typing import Annotated
from pydantic import BaseModel, Field
from starlette import status
from fastapi import APIRouter, Depends, HTTPException, Path
from ..models import Todos
from ..database import SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user

router= APIRouter(prefix='/admin',
    tags=['admin'])



def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]

@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role')!='admin':
        raise HTTPException(status_code=401, detail='Authentication failed')
        
    return db.query(models.Todos).all()
# created by me, delete a certain todo
@router.delete("/todo/delete/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency,db:db_dependency,todo_id:int=Path(gt=0)):
    if user is None or user.get('user_role')!='admin':
        raise HTTPException(status_code=401, detail='Authentication failed')
    todo_model=db.query(models.Todos).filter(models.Todos.id==todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found!")
    db.delete(todo_model)
    db.commit()
# created by me, delete a certain user by their id
@router.delete("/todo/delete_user/{owner_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user:user_dependency,db:db_dependency,owner_id:int=Path(gt=0)):
    if user is None or user.get('user_role')!='admin':
        raise HTTPException(status_code=401, detail='Authentication failed')
    user_model=db.query(models.Users).filter(models.Users.id==owner_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    db.query(models.Todos).filter(models.Todos.owner_id == owner_id).delete()
    db.delete(user_model)
    db.commit()
# created by me, get all users registered in the database
@router.get("/todo/show_users",status_code=status.HTTP_200_OK)
async def show_users(user:user_dependency,db:db_dependency):
    if user is None or user.get('user_role')!='admin':
        raise HTTPException(status_code=401, detail='Authentication failed')
    user_models=db.query(models.Users).all()
    return user_models


