from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Integer, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

app = FastAPI()

# task
# {"id": 1, "name": "Task1"}

engine = create_engine(
    "postgresql://fastapi_user:fastapi_pass@localhost:5433/fastapi_db",
    echo=True
)

class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    def __repr__(self):
        return f"<Task(id={self.id}, name='{self.name}')>"


Base.metadata.create_all(engine)


# Db Mock (In-memory data)
tasks_db = {
    1: {"id": 1, "name": "Task 1"},
    2: {"id": 2, "name": "Task 2"}
}
next_id = 3


class TaskCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100, description="Nazwa zadania")


class TaskUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Nazwa zadania")


class TaskResponse(BaseModel):
    id: int
    name: str


# C (Create) z CRUD
@app.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
def create_task(task: TaskCreate):
    """Stwórz nowe zadanie"""
    with Session(engine) as session:
        db_task = Task(name=task.name)

        session.add(db_task)
        session.commit()

        session.refresh(db_task)
    return db_task



# R (Read all) z CRUD
@app.get("/tasks", tags=["READ"])
def get_tasks():
    """Pobierz listę zadań"""
    with Session(engine) as session:
        stmt = select(Task)
        tasks = session.execute(stmt).scalars().all()

        tasks_list = [{"id": task.id, "name": task.name} for task in tasks]

    return {"tasks": tasks_list, "count": len(tasks_db)}


# R (Read detail) z CRUD
@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["READ"])
def get_task(task_id: int):
    """Pobierz pojedyncze zadanie"""
    with Session(engine) as session:
        task = session.get(Task, task_id)

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )

    return task


# U (Update) z CRUD
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate):
    """Zaktualizuj zadanie"""
    with Session(engine) as session:
        db_task = session.get(Task, task_id)

        if db_task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )
        db_task.name = task.name
        session.commit()
        session.refresh(db_task)

    return db_task

# D (Delete) z CRUD
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    """Usuń zadanie"""
    with Session(engine) as session:
        task = session.get(Task, task_id)

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )
        session.delete(task)
        session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
