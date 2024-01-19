from fastapi import FastAPI,Request,Depends,Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse,JSONResponse
from database import SessionLocal
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
# from models import base
from crud import create_item,delete_item
import models

app=FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount("/templates/static",StaticFiles(directory="templates/static"), name="static")

def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

#Get The Template Home Page
@app.get('/') 
def get_home(request:Request,db:Session = Depends(get_db)):
    new_expanses = db.query(models.Item).all()
    return templates.TemplateResponse("home.html",context={"request":request,"new_expanses":new_expanses})

# Create a new expense
@app.post('/create_expense')
async def create_expense(
        request: Request,
        expense_name: str = Form(...),
        date: str = Form(...),
        quantity: int = Form(...),
        price: int = Form(...),
        description: str = Form(...),
        db: Session = Depends(get_db)  # Use the dependency to get the database session
):
    item = create_item(db=db, expense_name=expense_name, date=date, quantity=quantity, price=price, description=description)
    return RedirectResponse(url='/',status_code=303)

# Delete an expense
@app.delete('/delete_expense/{id}')
async def delete_expense(
        request: Request,
        id: int,
        db: Session = Depends(get_db)  # Use the dependency to get the database session
):
    item = delete_item(db=db, id=id)
    new_expanses = db.query(models.Item).all()
    return jsonable_encoder(item)
    # return templates.TemplateResponse("home.html",context={"request":request,"new_expanses":new_expanses})

# Edit form for an expense
@app.post('/edit_expense_form/{id}')
async def edit_expense_form(
        request: Request,
        id: int,
        db: Session = Depends(get_db)  # Use the dependency to get the database session
):
    item = db.query(models.Item).filter(models.Item.id == id).first()
    return jsonable_encoder(item)


# Edit an expense
@app.put('/edit_expense/{id}')
async def edit_expense(
        request: Request,
        id: int ,
        expense_name: str = Form(...),
        date: str = Form(...),
        quantity: int = Form(...),
        price: int = Form(...),
        description: str = Form(...),
        db: Session = Depends(get_db)  # Use the dependency to get the database session
):
    item = delete_item(db=db, id=id)
    item = create_item(db=db, expense_name=expense_name, date=date, quantity=quantity, price=price, description=description)
    return RedirectResponse(url='/',status_code=303)