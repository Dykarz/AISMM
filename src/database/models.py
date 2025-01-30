from sqlalchemy import Column, Integer, String, JSON
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    password_hash = Column(String(200))  # Hashed
    auth_method = Column(String(20))     # 'api' o 'email'

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    profile_name = Column(String(50))
    social_connections = Column(JSON)    # Es: {'twitter': {'api_key': '...'}, 'instagram': {...}}