from sqlalchemy.orm import Session
from database import Base
from models import Item

# Create an item
def create_item(db: Session, expense_name: str, date: str, quantity: int, price: int, description: str):
    db_item = Item(expense_name=expense_name, date=date, quantity=quantity, price=price, description=description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Delete an item
def delete_item(db: Session, id: int):
    db_item = db.query(Item).filter(Item.id == id).first()
    db.delete(db_item)
    db.commit()
    return db_item