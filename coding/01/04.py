from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

app = FastAPI()

# task
# {"id": 1, "name": "Task1"}

# Db Mock (In-memory data)
tasks_db = {
    1: {"id": 1, "name": "Task 1"},
    2: {"id": 2, "name": "Task 2"}
}
next_id = 3


class TaskCreate(BaseModel):
    name: str = Field(min_length=10, max_length=100, description="Nazwa zadania")


class TaskUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Nazwa zadania")


class TaskResponse(BaseModel):
    id: int
    name: str


# C (Create) z CRUD
@app.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
def create_task(task: TaskCreate):
    """Stwórz nowe zadanie"""
    global next_id

    new_task = {
        "id": next_id,
        "name": task.name
    }
    tasks_db[next_id] = new_task
    next_id += 1
    return new_task


# R (Read all) z CRUD
@app.get("/tasks", tags=["READ"])
def get_tasks():
    """Pobierz listę zadań"""
    tasks_list = list(tasks_db.values())

    return {"tasks": tasks_db, "count": len(tasks_db)}


# R (Read detail) z CRUD
@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["READ"])
def get_task(task_id: int):
    """Pobierz pojedyncze zadanie"""
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )

    return tasks_db[task_id]


# U (Update) z CRUD
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate):
    """Zaktualizuj zadanie"""
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    tasks_db[task_id] = {"id": task_id, "name": task.name}
    return tasks_db[task_id]


# D (Delete) z CRUD
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Usuń zadanie"""
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )

    del tasks_db[task_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
