from sqlalchemy import Column, Integer, String
from database import Base,db_engine

class Item(Base): # Create a database model for the items table
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    expense_name = Column(String(255), index=True)
    date = Column(String(255))
    quantity = Column(Integer)
    price = Column(Integer)
    description = Column(String(255))
    
Base.metadata.create_all(bind=db_engine)