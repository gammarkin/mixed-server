import sys, os
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import app

client = TestClient(app)

def test_create_todo():
    response = client.post("/todos/", json={
        "title": "Test Todo",
        "description": "Test Description",
        "completed": False
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["completed"] is False

def test_get_todos():
    response = client.get("/todos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_todo():
    # create a todo
    create_resp = client.post("/todos/", json={
        "title": "Update Todo",
        "description": "To update",
        "completed": False
    })
    todo_id = create_resp.json()["id"]

    # update it
    update_resp = client.put(f"/todos/{todo_id}", json={
        "title": "Updated Todo",
        "description": "Updated",
        "completed": True
    })
    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated["title"] == "Updated Todo"
    assert updated["completed"] is True

def test_delete_todo():
    # Create a todo to delete
    create_resp = client.post("/todos/", json={
        "title": "Delete Todo",
        "description": "To delete",
        "completed": False
    })
    todo_id = create_resp.json()["id"]

    # Delete it
    delete_resp = client.delete(f"/todos/{todo_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json()["detail"] == "Todo deleted"