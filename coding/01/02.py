from fastapi import FastAPI


app = FastAPI()

# HTTP methods

# CRUD

@app.get("/items") # R
def get_items():
    """Pobierz listę elementów"""
    ...
    return {"items": []}


@app.post("/items")  # C
def create_item():
    """Stwórz nowy element"""
    ...
    return {"message": "Item created"}


@app.get("/items/{item_id}")  # R
def get_item(item_id: int):
    """Pobierz szczegóły elementu"""
    ...
    return {"item": item_id}


@app.put("/items/{item_id}")  # PUT = zastąp  # U
def update_item(item_id: int):
    """Zaktualizuj element"""
    ...
    return {"message": f"Item {item_id} updated (put)"}


@app.patch("/items/{item_id}")  # PATCH = popraw  # U
def update_item(item_id: int):
    """Zaktualizuj element"""
    ...
    return {"message": f"Item {item_id} updated (patch)"}


@app.delete("/items/{item_id}")  # D
def delete_item(item_id: int):
    ...
    """Usuń element"""
    return {"message": f"Item {item_id}  deleted"}


# custom status codes
from fastapi import status


@app.delete("/items", status_code=status.HTTP_204_NO_CONTENT)
def delete_item():
    ...
    """Usuń elementy"""
    return {"message": f"Items  deleted"}


from fastapi import HTTPException


@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {"user": user_id}

from fastapi import Body


# Body (post method)
@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(name = Body()):
    """Stwórz nowego użytkwonika"""
    return {"msg": f"User with {name} was created."}


# Headers
from fastapi import Header

# request's headers
@app.get("/tasks")
def get_headers(
    authorization: str = Header(None),
    user_agent: str = Header(None)
):
    """Odczyt headers z requestu"""
    return {
        "auth": authorization,
        "user_agent": user_agent
    }


from fastapi import Response


# respon's headers
@app.get("/tasks2")
def add_headers(response: Response):
    """Ustawiamy custor headers"""
    print(1/0)
    response.headers["Location"] = f"/tasks/name"
    response.headers["X-Custom-Header"] = "custom-value"
    return {"name": "task 1"}
