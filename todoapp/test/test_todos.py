from sqlalchemy import create_engine
from sqlalchemy import StaticPool
from ..database import Base
from ..main import app
from ..routers.todos import get_db,get_current_user 

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
    return {'username':'nikkupikku','id':1,'role':'admin'}

app.dependency_overrides[get_db]= override_get_db
app.dependency_overrides[get_current_user]= override_get_current_user


