from idlelib.configdialog import changes

from sqlalchemy.orm import Session, query

from app.models import Todo
from app.schemas import TodoCreate, TodoUpdate


def get_todos(db: Session, completed: bool | None = None) -> list[Todo]:
    query = db.query(Todo)

    if completed is not None:
        query = query.filter(Todo.completed == completed)

    return query.order_by(Todo.created_at.desc()).all()

def get_todo(db: Session, todo_id: str) -> Todo | None:
    return db.query(Todo).filter(Todo.id == todo_id).first()

def create_todo(db: Session, todo_data: TodoCreate) -> Todo:
    todo = Todo(**todo_data.model_dump());

    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def update_todo(db: Session, todo: Todo, todo_data: TodoUpdate) -> Todo:
    changes = todo_data.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)
    return todo

def delete_todo(db: Session, todo: Todo) -> None:
    db.delete(todo)
    db.commit()

def delete_completed_todo(db: Session) -> int:
    delete_count = (
    db.query(Todo)
        .filter(Todo.completed.is_(True))
        .delete(synchronize_session=False)
    )
    db.commit()
    return delete_count