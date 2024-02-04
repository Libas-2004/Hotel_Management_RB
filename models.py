from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, db_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base() # Create a base class for our models for two reasons: to inherit from it and to create a metadata object that will store the configuration of the database

class Item(Base): 
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    expense_name = Column(String(255), index=True)
    date = Column(String(255))
    quantity = Column(Integer)
    price = Column(Integer)
    description = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))  # Foreign key to relate to users table
    user = relationship("User", back_populates="items")

class User(Base): 
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), index=True)
    email= Column(String(255))  
    password = Column(String(255))
    items = relationship("Item", back_populates="user")  # Establish one-to-many relationship with items

Base.metadata.create_all(bind=db_engine)
