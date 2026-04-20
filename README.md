### Description

#### books.py and books2.py
- Basic set of python files which contain the code for dummy APIs created with FastAPI.
- books.py and books2.py are basic APIs which reference an internally defined list instead of a DB

#### todoapp folder:
- Contains a basic todoapp which references a sqlite db
# TodoApp — FastAPI Project Documentation
 
> **Context:** Built as part of a Udemy course on FastAPI. This is a RESTful backend for a todo list application with user authentication, JWT tokens, and a SQLite database.
 

 
## Project Structure
 
```
todoapp/
├── main.py               # App entry point — wires everything together
├── database.py           # SQLAlchemy engine, session, and Base setup
├── models.py             # ORM table definitions (Todos + Users)
├── todosapp.db           # SQLite database file (auto-created on first run)
├── routers/
│   ├── auth.py           # User registration, login, JWT token generation
│   └── todos.py          # CRUD operations for todos
└── venv/                 # Python virtual environment
```
 

 
## Tech Stack
 
| Tool | Purpose |
|------|---------|
| **FastAPI** | Web framework — defines HTTP routes and handles requests |
| **SQLAlchemy** | ORM — maps Python classes to database tables |
| **SQLite** | Lightweight file-based database (`todosapp.db`) |
| **Pydantic** | Request body validation via `BaseModel` |
| **Passlib / bcrypt** | Password hashing |
| **python-jose** | JWT token creation and decoding |
| **OAuth2PasswordBearer** | FastAPI's built-in OAuth2 token scheme |
 

 
## File-by-File Breakdown
 
### `database.py` — Database Foundation
 
This is the lowest layer of the project. It sets up three things:
 
1. **Engine** — The actual connection to the `todosapp.db` SQLite file. `check_same_thread: False` is required for SQLite with FastAPI because FastAPI handles concurrent requests.
2. **SessionLocal** — A factory that creates database sessions. A session is a temporary workspace for reading/writing — you open one per request, do your work, then close it.
3. **Base** — The declarative base that all model classes inherit from, so SQLAlchemy knows they represent database tables.
 

### `models.py` — Database Tables
 
Defines two tables as Python classes:
 
**`Todos` table**
```
id (PK) | title | description | priority | complete | owner_id (FK → users.id)
```
 
**`Users` table**
```
id (PK) | email (unique) | username (unique) | first_name | last_name | hashed_password | is_active | role
```
 
The `owner_id` field in `Todos` is a foreign key linking each todo to its creator. (Note: the relationship is declared in the DB schema but the current todo CRUD routes don't yet filter todos by the logged-in user — that's a natural next step.)
 

 
### `main.py` — App Entry Point
 
```python
app = FastAPI()
models.Base.metadata.create_all(bind=engine)  # Creates DB tables if they don't exist
app.include_router(auth.router)               # Registers /auth/* routes
app.include_router(todos.router)              # Registers todo CRUD routes
```
 
This is the composition root — it binds the database, models, and routers together. `create_all` is idempotent: safe to run on every startup, only creates tables that don't already exist.
 
---
 
### `routers/todos.py` — Todo CRUD
 
All routes operate directly on the `todos` table. Uses a **dependency injection pattern** for the database session:
 
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
db_dependency = Annotated[Session, Depends(get_db)]
```
 
This ensures the session is always closed after a request, even if an error occurs.
 
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Return all todos |
| GET | `/todo/{todo_id}` | Return a single todo by ID |
| POST | `/todo` | Create a new todo |
| PUT | `/todo/{todo_id}` | Update an existing todo |
| DELETE | `/todo/{todo_id}` | Delete a todo |
 
The `ToDoRequest` Pydantic model enforces validation:
- `title`: min 3 characters
- `description`: 3–100 characters
- `priority`: integer between 1 and 5
- `complete`: boolean
 
---
 
### `routers/auth.py` — Authentication
 
Handles user registration and JWT-based login.
 
**User Registration (`POST /auth/create_user`)**
Takes a `UserRequest` body, hashes the password with bcrypt, and stores the new user in the database.
 
**Login (`POST /auth/token`)**
Uses FastAPI's `OAuth2PasswordRequestForm` (username + password form fields). Verifies credentials, and if valid, generates a JWT access token valid for 20 minutes.
 
**Token (`create_access_token`)**
Encodes `username` and `user_id` into a JWT signed with a secret key using the HS256 algorithm.
 
**Auth Guard (`get_current_user`)**
A dependency function that decodes the JWT from the `Authorization: Bearer <token>` header on any protected route. Returns the current user's `username` and `id`, or raises a 401 if the token is invalid or expired.
 
---
 
## Control Flow
 
### 1. App Startup
```
uvicorn main:app
  → create_all() checks DB, creates tables if missing
  → Routers registered: /auth/* and todo routes
```
 
### 2. New User Registration
```
POST /auth/create_user
  → Pydantic validates UserRequest body
  → bcrypt hashes the password
  → New Users row inserted into DB
  → 201 Created response
```
 
### 3. Login & Token Flow
```
POST /auth/token  (form: username + password)
  → authenticate_user() queries DB for username
  → bcrypt.verify() checks password against stored hash
  → If valid: create_access_token() builds JWT (expires 20 min)
  → Returns { access_token, token_type: "bearer" }
```
 
### 4. Authenticated Request (future pattern)
```
GET /todo  (with Authorization: Bearer <token>)
  → oauth2_bearer extracts token from header
  → get_current_user() decodes JWT → { username, id }
  → Route handler receives current user + DB session
  → Queries todos (optionally filtered by owner_id)
```
 
### 5. Create / Update / Delete Todo
```
POST /todo  (body: title, description, priority, complete)
  → Pydantic validates ToDoRequest
  → models.Todos(**request.model_dump()) creates ORM object
  → db.add() + db.commit() persists to SQLite
  → 201 Created / 204 No Content
```
 
---
 
## Key Concepts Used
 
**Dependency Injection (`Depends`)** — FastAPI resolves dependencies automatically. `get_db` is called per request, yielding a session that is always cleaned up. `get_current_user` is a reusable auth guard that any route can add as a dependency.
 
**ORM vs Raw SQL** — SQLAlchemy lets you work with Python objects (`db.query(Todos).filter(...)`) instead of writing SQL strings. The model class definition is the single source of truth for the table schema.
 
**JWT Authentication** — Stateless auth: the server doesn't store sessions. The token itself contains the user's identity (encoded + signed), so any valid token is enough to identify the user. The 20-minute expiry limits the damage from stolen tokens.
 
**Pydantic Validation** — Request bodies are automatically validated before the handler runs. If `priority` is 6 or `title` is 1 character, FastAPI returns a 422 with clear error details — no manual validation code needed.
 
**Router Prefixes** — `APIRouter(prefix='/auth', tags=['auth'])` groups auth routes cleanly. The `/auth` prefix is added automatically to all routes in that file.
 

 
## Current Limitations / Natural Next Steps
 

1. **Secret key is hardcoded** — In production, this should come from an environment variable.
2. **No refresh tokens** — Tokens expire in 20 minutes with no way to renew without re-logging in.
 

 
## Summary
 
This project is a FastAPI backend for a todo application that demonstrates a clean separation of concerns across three layers:
 
The **data layer** (`database.py` + `models.py`) uses SQLAlchemy to define two tables — users and todos — connected by a foreign key. SQLite serves as the database, with the engine and session configured in `database.py`.
 
The **routing layer** (`routers/`) splits business logic into two files: `todos.py` handles standard CRUD operations on todos with Pydantic validation, while `auth.py` handles the full authentication lifecycle — registration, password hashing with bcrypt, JWT token generation on login, and a reusable `get_current_user` dependency for protecting routes.
`users.py` handles all the user routes- including password change api endpoints and user information aquisition.
`admin.py` handles all admin-related routes, including the ability to read all users from the user table, delete a user and delete a todo.

 
The **entry point** (`main.py`) wires everything together: it creates database tables on startup and registers both routers with the FastAPI app.
 
The most important architectural pattern used throughout is **FastAPI's dependency injection system** — particularly the `get_db` session pattern, which guarantees safe database session lifecycle management on every request, and `get_current_user`, which provides a clean, reusable way to protect any route with authentication.
