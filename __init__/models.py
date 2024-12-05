from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# User table model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    structures = relationship("Structure", back_populates="user")

# Structure table model
class Structure(Base):
    __tablename__ = 'structures'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    num_nodes = Column(Integer)
    num_edges = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_dag = Column(Boolean, default=True)

    user = relationship("User", back_populates="structures")

# Create a namespace for the models
class models:
    User = User
    Structure = Structure
