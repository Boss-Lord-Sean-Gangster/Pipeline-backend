# main.py (FastAPI routes)

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import database, auth, models

app = FastAPI()

# OAuth2PasswordBearer: Used to extract the token from request headers
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Token endpoint for login
@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Register user (sign up)
@app.post("/register")
def register_user(email: str, password: str, db: Session = Depends(database.get_db)):
    # Check if the user already exists
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered")
    
    # Create new user
    new_user = auth.create_user(db, email, password)
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
