# auth.py (authentication logic)

from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import models
import os
from dotenv import load_dotenv

# Password encryption using passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key for JWT token (you should keep it secret)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Hash the password before storing it
def hash_password(password: str):
    return pwd_context.hash(password)

# Verify hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Create access token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Register a user
def create_user(db: Session, email: str, password: str):
    hashed_password = hash_password(password)
    db_user = models.User(email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Authenticate user
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None
