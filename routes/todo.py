from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from db.sqlite import DATABASE, init_db

router = APIRouter()

class Todo(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

def get_db():
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# initialize DB when the router is imported
init_db()

@router.get("/", response_model=List[Todo])
def get_todos(conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.execute("SELECT id, title, description, completed FROM todos ORDER BY id DESC")
    return [Todo(**dict(row)) for row in cursor.fetchall()]

@router.get("/{todo_id}", response_model=Todo)
def get_todo(todo_id: int, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.execute("SELECT id, title, description, completed FROM todos WHERE id = ?", (todo_id,))
    row = cursor.fetchone()
    if row:
        return Todo(**dict(row))
    raise HTTPException(status_code=404, detail="Todo not found")

@router.post("/", response_model=Todo)
def create_todo(todo: Todo, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.execute(
        "INSERT INTO todos (title, description, completed) VALUES (?, ?, ?)",
        (todo.title, todo.description, int(todo.completed))
    )
    conn.commit()
    todo.id = cursor.lastrowid
    return todo

@router.patch("/{todo_id}", response_model=Todo)
def patch_todo(todo_id: int, todo: Todo, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.execute("SELECT id, title, description, completed FROM todos WHERE id = ?", (todo_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    existing_todo = Todo(**dict(row))
    updated_todo = todo.dict(exclude_unset=True)
    for key, value in updated_todo.items():
        setattr(existing_todo, key, value)
    
    conn.execute(
        "UPDATE todos SET title = ?, description = ?, completed = ? WHERE id = ?",
        (existing_todo.title, existing_todo.description, int(existing_todo.completed), todo_id)
    )
    conn.commit()
    return existing_todo

@router.put("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: Todo, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.execute(
        "UPDATE todos SET title = ?, description = ?, completed = ? WHERE id = ?",
        (updated_todo.title, updated_todo.description, int(updated_todo.completed), todo_id)
    )
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    conn.commit()
    updated_todo.id = todo_id
    return updated_todo

@router.delete("/{todo_id}", response_model=dict)
def delete_todo(todo_id: int, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    conn.commit()
    return {"detail": "Todo deleted"}
