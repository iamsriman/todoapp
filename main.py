from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from . import models, schemas, crud, auth

Base.metadata.create_all(bind=engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = auth.decode_token(token)
        user_id = payload.get("user_id")
        return db.query(models.User).get(user_id)
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(400, "Email already registered")
    return crud.create_user(db, user.email, user.password)

@app.post("/login", response_model=schemas.Token)
def login(data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(401, "Invalid credentials")
    token = auth.create_access_token({"user_id": user.id})
    return {"access_token": token}

@app.post("/todos")
def add_todo(todo: schemas.TodoCreate, user=Depends(get_current_user), db=Depends(get_db)):
    return crud.create_todo(db, todo.title, user.id)

@app.get("/todos", response_model=list[schemas.TodoOut])
def get_todos(user=Depends(get_current_user), db=Depends(get_db)):
    return crud.get_todos(db, user.id)


@app.put("/todos/{todo_id}")
def update(todo_id: int, data: schemas.TodoUpdate,
           user=Depends(get_current_user), db=Depends(get_db)):
    todo = crud.update_todo(db, todo_id, user.id, data)
    if not todo:
        raise HTTPException(404, "Todo not found")
    return todo

@app.delete("/todos/{todo_id}")
def delete(todo_id: int, user=Depends(get_current_user), db=Depends(get_db)):
    if not crud.delete_todo(db, todo_id, user.id):
        raise HTTPException(404, "Todo not found")
    return {"message": "Deleted"}
