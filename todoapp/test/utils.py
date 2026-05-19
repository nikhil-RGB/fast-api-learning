from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..database import Base
from ..main import app
from ..models import Todos
import pytest
SQL_ALCHEMY_DATABASE_URL="sqlite:///./testdb.db"
engine= create_engine(SQL_ALCHEMY_DATABASE_URL,
                      connect_args={"check_same_thread":False},
                      poolclass=StaticPool,
                     )

TestingSessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

#Override dependency injection here-->
def override_get_db():
    db= TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

#Override function for getting current user-->
def  override_get_current_user():
    return {'username':'nikkupikku','id':1,'user_role':'admin'}


client=TestClient(app)

#Fixture for creating a test-todo and then deleting it
@pytest.fixture
def test_todo():
    todo= Todos(
        title="Learn to code",
        description="Need to learn everyday",
        priority=5,
        owner_id=1,
        id=1,
    )
    db=TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()
