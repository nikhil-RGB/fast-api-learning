""" 
Note: Comments added in from Claude, to explain the code for database.py
These pull in tools from SQLAlchemy, which is Python's most popular ORM library.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")


""" 
This is simply the address of your database. Think of it like a file path. You're using SQLite, which is a lightweight database that lives as a single file (todos.db) right in your project folder. When you run the app, this file gets created automatically if it doesn't already exist.
"""
SQLALCHEMY_DATABASE_URL=os.getenv("DATABASE_URL")

""" 
The engine is the actual connection to your database — it's what "powers" all communication between your app and the todos.db file.
The check_same_thread: False part is a SQLite-specific setting that tells it "allow multiple parts of the app to use this connection at the same time" — necessary for FastAPI since it handles multiple requests concurrently.
"""
engine= create_engine(SQLALCHEMY_DATABASE_URL)

"""
A session is like a temporary workspace or a conversation with your database. Every time a user makes a request to your API, you'll open a session, do your database work (read/write data), then close it.

autocommit=False — changes aren't saved automatically; you have to explicitly say "save this" (gives you more control)
autoflush=False — similarly, data isn't pushed to the DB until you're ready
bind=engine — connects this session to the engine you created above
"""
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)


"""
This is the foundation for all your database models (tables). When you create a Todos table later, your class will inherit from this Base. That's how SQLAlchemy knows it should be treated as a database table.
Think of Base as a blueprint template that all your future tables will be built from.
"""
Base =declarative_base()