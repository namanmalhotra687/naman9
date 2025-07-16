# main.py

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
from model import Base, engine
import controller  # ✅ This must contain router with @router.put() functions

# ✅ Step 1: Create FastAPI app
app = FastAPI(debug=True)

# ✅ Step 2: Add middleware
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

# ✅ Step 3: Templates
templates = Jinja2Templates(directory="templates")

# ✅ Step 4: Include your controller router
app.include_router(controller.router)

# ✅ Step 5: Create database tables
Base.metadata.create_all(bind=engine)

# ✅ Step 6: Add your endpoints (login, add, edit, etc.) BELOW this

app.include_router(controller.router)


app = FastAPI(debug=True)
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
templates = Jinja2Templates(directory="templates")

# Create tables
Base.metadata.create_all(bind=engine)

# -------------------- LOGIN / LOGOUT --------------------

@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/login", response_class=HTMLResponse)
def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    if username in ["admin", "naman"] and password == "123":
        request.session['user'] = username
        return templates.TemplateResponse("welcome.html", {"request": request, "username": username})
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)

# -------------------- HOME --------------------

@app.get("/home", response_class=HTMLResponse)
def home(request: Request, db=Depends(controller.get_db)):
    if "user" not in request.session:
        return RedirectResponse("/login")
    return controller.show_home(request, db)

# -------------------- FORM SUBMIT --------------------

@app.post("/add")
def add(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    db=Depends(controller.get_db)
):
    if "user" not in request.session:
        return RedirectResponse("/login", status_code=303)

    username = request.session['user']
    controller.add_item(title, description, username, db)
    return RedirectResponse("/home", status_code=303)

# -------------------- CRUD JSON --------------------

class ItemSchema(BaseModel):
    title: str
    description: str
    username: str

@app.post("/add-json")
def add_json(item: ItemSchema, db=Depends(controller.get_db)):
    controller.add_item(item.title, item.description, item.username, db)
    return {"message": "Item added via JSON"}

@app.get("/items")
def get_items(db=Depends(controller.get_db)):
    return controller.get_all_items(db)

@app.get("/")
def root():
    return RedirectResponse("/login")


@app.post("/edit/{item_id}")
def edit_item(
    item_id: int,
    title: str = Form(...),
    description: str = Form(""),
    username: str = Form(...),
    status: str = Form(...),
    deadline: str = Form(None),
    request: Request = None,
    db=Depends(controller.get_db)
):
    if "user" not in request.session:
        return RedirectResponse("/login", status_code=303)

    controller.update_item(item_id, title, description, username, status, deadline, db)
    return RedirectResponse("/home", status_code=303)


@app.post("/edit/{item_id}")
def edit_item(
    item_id: int,
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    username: str = Form(...),
    status: str = Form(...),
    deadline: str = Form(""),
    db=Depends(controller.get_db)
):
    if "user" not in request.session:
        return RedirectResponse("/login", status_code=303)

    controller.update_item(item_id, title, description, username, status, deadline, db)
    return RedirectResponse("/home", status_code=303)

@app.get("/delete/{item_id}")
def delete_item(item_id: int, request: Request, db=Depends(controller.get_db)):
    if "user" not in request.session:
        return RedirectResponse("/login", status_code=303)

    controller.delete_item(item_id, db)
    return RedirectResponse("/home", status_code=303)

from fastapi.responses import HTMLResponse

@app.post("/edit/{item_id}", response_class=HTMLResponse)
def edit_item(
    request: Request,
    item_id: int,
    title: str = Form(...),
    description: str = Form(...),
    username: str = Form(...),
    status: str = Form(...),
    deadline: str = Form(...),
    db=Depends(controller.get_db)
):
    controller.update_item(item_id, title, description, username, status, deadline, db)
    items = controller.get_all_items(db)
    return templates.TemplateResponse("home.html", {
        "request": request,
        "items": items,
        "message": "✅ Task updated successfully!"
    })

@app.get("/welcome")
def welcome(request: Request):
    if "user" not in request.session:
        return RedirectResponse("/login")
    return templates.TemplateResponse("welcome.html", {"request": request})

from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    username = Column(String)
    status = Column(String)
    deadline = Column(String)


from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from model import Base, engine
import controller
from controller import get_db
from pydantic import BaseModel

app = FastAPI(debug=True)
app.add_middleware(SessionMiddleware, secret_key="secret")
templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)
app.include_router(controller.router)

@app.get("/", response_class=HTMLResponse)
def root():
    return RedirectResponse("/login")

@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/login", response_class=HTMLResponse)
def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    if username in ["admin", "naman"] and password == "123":
        request.session["user"] = username
        return templates.TemplateResponse("welcome.html", {"request": request, "username": username})
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)

from collections import Counter
from controller import get_all_items

from collections import Counter

from collections import Counter

@app.get("/home", response_class=HTMLResponse)
def home(request: Request, db=Depends(get_db)):
    if "user" not in request.session:
        return RedirectResponse("/login")

    items = get_all_items(db)

    # Status chart
    status_counts = Counter([item.status for item in items if item.status])
    status_labels = list(status_counts.keys())
    status_values = list(status_counts.values())

    # Category chart
    category_counts = Counter([item.description for item in items if item.description])
    category_labels = list(category_counts.keys())
    category_values = list(category_counts.values())

    return templates.TemplateResponse("home.html", {
        "request": request,
        "items": items,
        "labels": status_labels,
        "values": status_values,
        "cat_labels": category_labels,
        "cat_values": category_values
    })



@app.post("/add")
def add(request: Request, title: str = Form(...), description: str = Form(""), db=Depends(get_db)):
    if "user" not in request.session:
        return RedirectResponse("/login", status_code=303)
    username = request.session["user"]
    controller.add_item(title, description, username, db)
    return RedirectResponse("/home", status_code=303)

@app.get("/delete/{item_id}")
def delete_item(item_id: int, request: Request, db=Depends(get_db)):
    if "user" not in request.session:
        return RedirectResponse("/login", status_code=303)
    controller.delete_item(item_id, db)
    return RedirectResponse("/home", status_code=303)

@app.post("/edit/{item_id}", response_class=HTMLResponse)
def edit_item(request: Request, item_id: int, title: str = Form(...), description: str = Form(""), username: str = Form(...), status: str = Form(...), deadline: str = Form(""), db=Depends(get_db)):
    if "user" not in request.session:
        return RedirectResponse("/login", status_code=303)
    controller.update_item(item_id, title, description, username, status, deadline, db)
    items = controller.get_all_items(db)
    return templates.TemplateResponse("home.html", {"request": request, "items": items, "message": "✅ Task updated successfully!"})

@app.get("/items")
def get_items(db=Depends(get_db)):
    return controller.get_all_items(db)

@app.get("/welcome", response_class=HTMLResponse)
def welcome(request: Request):
    if "user" not in request.session:
        return RedirectResponse("/login")
    return templates.TemplateResponse("welcome.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db=Depends(controller.get_db)):
    if "user" not in request.session:
        return RedirectResponse("/login")

    items = controller.get_all_items(db)
    
    # Count status
    status_counts = {"New": 0, "In Progress": 0, "Done": 0}
    for item in items:
        status_counts[item.status] = status_counts.get(item.status, 0) + 1

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "status_counts": status_counts
    })


from generator_logic import generate_task

@app.get("/generate", response_class=HTMLResponse)
def generate_form(request: Request):
    if "user" not in request.session:
        return RedirectResponse("/login")
    return templates.TemplateResponse("generate.html", {"request": request})

@app.post("/generate", response_class=HTMLResponse)
def generate_post(request: Request, local_kw: str = Form(""), db=Depends(controller.get_db)):
    if "user" not in request.session:
        return RedirectResponse("/login")

    task = generate_task(local_kw)
    controller.add_item(task['title'], task['description'], task['username'], db)
    controller.update_item(
        item_id=db.query(controller.Item).order_by(controller.Item.id.desc()).first().id,
        title=task['title'],
        description=task['description'],
        username=task['username'],
        status=task['status'],
        deadline=task['deadline'],
        db=db
    )
    return RedirectResponse("/home", status_code=303)

from scheduler import start_scheduler

start_scheduler()

from fastapi.responses import StreamingResponse
import csv
import io

@app.get("/export")
def export_csv(db=Depends(get_db)):
    items = controller.get_all_items(db)
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["ID", "Title", "Description", "Username", "Status", "Deadline"])
    for item in items:
        writer.writerow([item.id, item.title, item.description, item.username, item.status, item.deadline])
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=tasks.csv"})
    from fastapi.responses import HTMLResponse
from fastapi import Request
from controller import get_db, get_all_items
from collections import Counter

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db=Depends(get_db)):
    if "user" not in request.session:
        return RedirectResponse("/login")

    items = get_all_items(db)
    status_counts = Counter([item.status for item in items if item.status])

    labels = list(status_counts.keys())
    values = list(status_counts.values())

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "labels": labels,
        "values": values
    })

from fastapi.responses import RedirectResponse

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/login")
