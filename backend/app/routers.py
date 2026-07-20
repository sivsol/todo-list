from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import crud
from app.dependencies import get_db
from app.schemas import TodoRead, TodoCreate, TodoUpdate

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("", response_model=list[TodoRead])
def list_todos(completed: bool | None = Query(default=None), db: Session = Depends(get_db),):
    return crud.get_todos(db, completed=completed)

@router.post("", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
def add_todo(todo_data: TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo_data)

@router.delete("/completed")
def clear_completed_todo(db: Session = Depends(get_db)):
    deleted_count = crud.delete_completed_todo(db)

    return {
        "message": "已清除完成任务",
        "deleted_count": deleted_count,
    }

@router.get("/{todo_id}", response_model=TodoRead)
def get_todo(todo_id: str, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="任务不存在")

    return todo

@router.patch("/{todo_id}", response_model=TodoRead)
def edit_todo(
        todo_id: str,
        todo_data: TodoUpdate,
        db: Session = Depends(get_db),
):
    todo = crud.get_todo(db, todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="任务不存在")

    return crud.update_todo(db, todo, todo_data)

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_todo(todo_id: str, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="任务不存在")

    crud.delete_todo(db, todo)