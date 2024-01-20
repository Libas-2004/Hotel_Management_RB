from sqlalchemy.orm import Session
from models import Item # Import the Item model we created

# Create an item
def create_item(db: Session, expense_name: str, date: str, quantity: int, price: int, description: str):
    db_item = Item(expense_name=expense_name, date=date, quantity=quantity, price=price, description=description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Delete an item
def delete_item(db: Session, id: int):
    db_item = db.query(Item).filter(Item.id == id).first() # Get the item from the database with the id passed in the url
    db.delete(db_item)
    db.commit()
    return db_item