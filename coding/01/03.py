from fastapi import Body, FastAPI, HTTPException, Response, status


app = FastAPI()

# task
# {"id": 1, "name": "Task1"}

# Db Mock (In-memory data)
tasks_db = {
    1: {"id": 1, "name": "Task 1"},
    2: {"id": 2, "name": "Task 2"}
}
next_id = 3


# C (Create) z CRUD
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(name: str = Body()):
    """Stwórz nowe zadanie"""
    global next_id

    new_task = {
        "id": next_id,
        "name": name
    }
    tasks_db[next_id] = new_task
    next_id += 1
    return new_task


# R (Read all) z CRUD
@app.get("/tasks")
def get_tasks():
    """Pobierz listę zadań"""
    tasks_list = list(tasks_db.values())

    return {"tasks": tasks_db, "count": len(tasks_db)}


# R (Read detail) z CRUD
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Pobierz pojedyncze zadanie"""
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )

    return tasks_db[task_id]


# U (Update) z CRUD
@app.put("/tasks/{task_id}")
def update_task(task_id: int, name: str = Body()):
    """Zaktualizuj zadanie"""
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    tasks_db[task_id] = {"id": task_id, "name": name}
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
