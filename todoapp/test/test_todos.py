
from ..routers.todos import get_db,get_current_user 
from fastapi import status
from ..models import Todos
from .utils import *



app.dependency_overrides[get_db]= override_get_db
app.dependency_overrides[get_current_user]= override_get_current_user


# test for api endpoint "/"
def test_read_all_authenticated(test_todo):
    response=client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete':False, 'title':'Learn to code','description':"Need to learn everyday", 'priority':5,'id':1,'owner_id':1}]

# test for what happens when a todo is not found
def test_todo_not_found(test_todo):
    response=client.get("/todo/999")
    assert response.status_code== status.HTTP_404_NOT_FOUND
    assert response.json()=={'detail':'Todo not found'}

#test for creation of todo object
def test_todo_creation(test_todo):
    todo_req={
        'title':'Test todo',
        'description':'Test todo description',
        'priority':2,
        'complete':False,
    }
    response=client.post("/todo",json=todo_req)
    assert response.status_code==status.HTTP_201_CREATED

    db=TestingSessionLocal()
    todo_model=db.query(Todos).filter(Todos.id==2).first()
    # Assertions to check if the todo item actually exists in the test table
    assert todo_model.title==todo_req.get('title')
    assert todo_model.description==todo_req.get('description')
    assert todo_model.priority==todo_req.get('priority')
    assert todo_model.complete==todo_req.get('complete')

#test for updation of an existing todo entry
def test_todo_updation(test_todo):
    todo_req={
        'title':'Updated Test todo',
        'description':'Updated Test todo description',
        'priority':2,
        'complete':True,
    }
    response=client.put("/todo/1",json=todo_req)
    assert response.status_code==status.HTTP_204_NO_CONTENT
    db=TestingSessionLocal()
    todo_model=db.query(Todos).filter(Todos.id==1).first()
    assert todo_model.title==todo_req.get('title')
    assert todo_model.description==todo_req.get('description')
    assert todo_model.priority==todo_req.get('priority')
    assert todo_model.complete==todo_req.get('complete')
    
# Test for failed put operation
def test_update_todo_not_found(test_todo):
    todo_req={
        'title':'Updated Test todo',
        'description':'Updated Test todo description',
        'priority':2,
        'complete':True,
    }
    response=client.put("/todo/999",json=todo_req)
    assert response.status_code==status.HTTP_404_NOT_FOUND
    assert response.json()=={'detail':'Todo not found'}
# Test for deletion operation
def test_delete_todo(test_todo):
    response=client.delete("/todo/1")
    assert response.status_code==status.HTTP_204_NO_CONTENT
    db=TestingSessionLocal()
    todo_model=db.query(Todos).filter(Todos.id==1).first()
    assert todo_model is None
# Test for todo not found when deletion requested
def test_delete_todo_not_found():
    response = client.delete('/todos/todo/999')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}












