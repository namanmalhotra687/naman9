import os
print("➡ Current Working Directory:", os.getcwd())
print("➡ Templates Exist:", os.path.exists("templates/home.html"))
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from model import SessionLocal, Item
from fastapi.templating import Jinja2Templates



templates = Jinja2Templates(directory="templates")

import os
print("📁 Template path:", os.path.abspath("templates"))


templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def show_home(request: Request, db: Session):
    items = db.query(Item).all()
    title = request.query_params.get("title", "")
    description = request.query_params.get("description", "")
    username = request.query_params.get("username", "")
    return templates.TemplateResponse("home.html", {
        "request": request,
        "items": items,
        "submitted_title": title,
        "submitted_description": description,
        "submitted_username": username
    })



def add_item(title: str, description: str, username: str, db: Session):
    new_item = Item(title=title, description=description, username=username)
    db.add(new_item)
    db.commit()
    return RedirectResponse(
        url=f"/home?title={title}&description={description}&username={username}",
        status_code=303
    )


def delete_item(item_id: int, db: Session):
    item = db.query(Item).get(item_id)
    if item:
        db.delete(item)
        db.commit()


def edit_item(item_id: int, title: str, description: str, username: str, db: Session):
    item = db.query(Item).get(item_id)
    if item:
        item.title = title
        item.description = description
        item.username = username
        db.commit()


def get_all_items(db: Session):
    return db.query(Item).all()

def show_home(request: Request, db: Session):
    print("✅ Entered show_home")
    items = db.query(Item).all()
    print(f"🧠 Found {len(items)} items")
    
    return templates.TemplateResponse("home.html", {
        "request": request,
        "items": items
    })

def update_item(item_id: int, title: str, description: str, username: str, status: str, deadline: str, db: Session):
    item = db.query(Item).get(item_id)
    if item:
        item.title = title
        item.description = description
        item.username = username
        item.status = status
        item.deadline = deadline
        db.commit()




# controller.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from model import SessionLocal, Item
from pydantic import BaseModel
from datetime import date

router = APIRouter()

class UpdateTask(BaseModel):
    status: str
    deadline: date  # or str if you're storing it as string

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.put("/edit-json/{item_id}")
def update_task(item_id: int, task: UpdateTask, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.status = task.status
    item.deadline = task.deadline
    db.commit()
    return {"message": "✅ Task updated"}

from fastapi import Request, Depends, APIRouter, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from model import SessionLocal, Item

templates = Jinja2Templates(directory="templates")
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from model import Item

templates = Jinja2Templates(directory="templates")

def show_home(request: Request, db: Session):
    items = db.query(Item).all()

    # 🧠 Compute task counts
    completed = sum(1 for i in items if i.status == "Done")
    pending = sum(1 for i in items if i.status in ("New", "In Progress"))
    overdue = sum(1 for i in items if i.status != "Done" and i.deadline and i.deadline < date.today())

    # 🧠 Compute categories
    categories = list(set(item.description for item in items if item.description))
    category_counts = [sum(1 for item in items if item.description == cat) for cat in categories]

    return templates.TemplateResponse("home.html", {
        "request": request,
        "items": items,
        "completed_tasks": completed or 0,
        "pending_tasks": pending or 0,
        "overdue_tasks": overdue or 0,
        "categories": categories or [],
        "category_counts": category_counts or []
    })



def add_item(title: str, description: str, username: str, db: Session):
    new_item = Item(title=title, description=description, username=username)
    db.add(new_item)
    db.commit()

def delete_item(item_id: int, db: Session):
    item = db.query(Item).get(item_id)
    if item:
        db.delete(item)
        db.commit()

def update_item(item_id: int, title: str, description: str, username: str, status: str, deadline: str, db: Session):
    item = db.query(Item).get(item_id)
    if item:
        item.title = title
        item.description = description
        item.username = username
        item.status = status
        item.deadline = deadline
        db.commit()

def get_all_items(db: Session):
    return db.query(Item).all()

# JSON PUT API
class UpdateTask(BaseModel):
    status: str
    deadline: str

@router.put("/edit-json/{item_id}")
def update_task_json(item_id: int, task: UpdateTask, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.status = task.status
    item.deadline = task.deadline
    db.commit()
    return {"message": "✅ Task updated via JSON"}

from fastapi import Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

@router.get("/view", response_class=HTMLResponse)
def view_page(request: Request, db: Session = Depends(get_db)):
    if "user" not in request.session:
        return RedirectResponse("/login", status_code=303)
    
    items = get_all_items(db)
    return templates.TemplateResponse("home.html", {
        "request": request,
        "items": items
    })
