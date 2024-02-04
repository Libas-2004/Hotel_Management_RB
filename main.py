from fastapi import FastAPI,Request,Depends,Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse,JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from crud import create_item,delete_item # Import the CRUD operations we created
from database import SessionLocal # Import the database session we created
import models # Import the database models we created

app=FastAPI() # Create a FastAPI instance
templates = Jinja2Templates(directory='templates') # Create a Jinja2Templates object and set the directory to the templates folder
app.mount("/templates/static",StaticFiles(directory="templates/static"), name="static") # Mount the static files folder to the templates/static folder

def get_db(): # Create a dependency function that will return the database session
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.middleware("http") # Create a middleware that will add a header to all responses
async def add_header(request: Request, call_next):
    protected_routes = ["/getform","/create_expense","/delete_expense","/edit_expense_form","/edit_expense","/search_expens"]
    if request.url.path in protected_routes:
       request.headers = {"Authorization ": "Bearer token"}
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response
    

@app.get('/')  # get the home page of the application and render the signup.html template
def get_home(request:Request):
    return templates.TemplateResponse("signup.html",context={"request":request})

@app.post('/signup')  # Create a new user and redirect to the home page
async def signup(
        request: Request,
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)  # Use the dependency to get the database session
):
    user = models.User(username=username,email=email, password=password)
    db.add(user)
    db.commit()
    return RedirectResponse(url='/getform',status_code=303) # redirect to the home page

@app.get('/login')  # get the home page of the application and render the login.html template
def get_login(request:Request):
    return templates.TemplateResponse("login.html",context={"request":request})

@app.post('/login')  # get the home page of the application and render the login.html template
async def login(
    request: Request,
    email:str = Form(...),
    password:str = Form(...),
    db: Session = Depends(get_db)  # Use the dependency to get the database session
):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        return JSONResponse(status_code=404,content={"message":"user not found"})
    if user.password != password:
        return JSONResponse(status_code=404,content={"message":"password is incorrect"})
    return RedirectResponse(url='/getform',status_code=303)

#Get The Template Home Page
@app.get('/getform')  # get the home page of the application and render the home.html template
def get_home(request:Request,db:Session = Depends(get_db)):
    new_expanses = db.query(models.Item).all()
    return templates.TemplateResponse("home.html",context={"request":request,"new_expanses":new_expanses})

# Create a new expense
@app.post('/create_expense')# Create a new expense and redirect to the home page
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
    return RedirectResponse(url='/getform',status_code=303) # redirect to the home page

# Delete an expense
@app.delete('/delete_expense/{id}')
async def delete_expense(
        request: Request,
        id: int,
        db: Session = Depends(get_db)  # Use the dependency to get the database session
):
    item = delete_item(db=db, id=id)
    return jsonable_encoder(item)

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
    delete_item(db=db, id=id)
    create_item(db=db, expense_name=expense_name, date=date, quantity=quantity, price=price, description=description)
    return RedirectResponse(url='/getform',status_code=303)

#for search
@app.get('/search_expens/{name}')
async def search_expens(
        request: Request,
        name: str,
        db: Session = Depends(get_db)  # Use the dependency to get the database session
):
    item = db.query(models.Item).having(models.Item.expense_name == name).first()   
    if item is None:
        return JSONResponse(status_code=404,content={"message":"item not found"})
    return jsonable_encoder(item)   
