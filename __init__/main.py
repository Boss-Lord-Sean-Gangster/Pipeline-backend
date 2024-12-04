# main.py (FastAPI routes)

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .auth import auth  # Importing the `auth` object from `auth.py`
from .database import get_db  # Importing `get_db` from `database.py`
from .models import models  # Importing models from `models.py`

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can replace "*" with specific origins, e.g., ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# OAuth2PasswordBearer: Used to extract the token from request headers
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class RegisterRequest(BaseModel):
    email: str
    password: str

# Token endpoint for login
@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Register user (sign up)
@app.post("/register")
def register_user(request: RegisterRequest, db: Session = Depends(get_db)):
    # Use request.email and request.password to access the data
    # Check if the user already exists
    existing_user = db.query(models.User).filter(models.User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered")
    
    # Create new user
    new_user = auth.create_user(db, request.email, request.password)
    return {"msg": "User created successfully", "user": new_user.email}

@app.get('/')
def getting():
    return {"Ping": "Pong"}

@app.post('/pipelines/parse')
async def parse_pipeline(pipeline: dict):
    nodes = pipeline.get("nodes", [])
    edges = pipeline.get("edges", [])
    num_nodes = len(nodes)
    num_edges = len(edges)

    return {"num_nodes": num_nodes, "num_edges": num_edges}
