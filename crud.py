from sqlalchemy.orm import Session
from .models import User, Todo
from .auth import hash_password, verify_password

def create_user(db: Session, email: str, password: str):
    user = User(email=email, password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        return None
    return user

def create_todo(db: Session, title: str, user_id: int):
    todo = Todo(title=title, user_id=user_id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def get_todos(db: Session, user_id: int):
    return db.query(Todo).filter(Todo.user_id == user_id).all()

def update_todo(db: Session, todo_id: int, user_id: int, data):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()
    if not todo:
        return None
    if data.title is not None:
        todo.title = data.title
    if data.completed is not None:
        todo.completed = data.completed
    db.commit()
    db.refresh(todo)
    return todo

def delete_todo(db: Session, todo_id: int, user_id: int):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()
    if not todo:
        return None
    db.delete(todo)
    db.commit()
    return True
