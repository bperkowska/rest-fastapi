from fastapi import FastAPI


app = FastAPI()


# path operation
# http://127.0.0.1:8000/
@app.get("/")
def read_root():
    return {"message": "Hello world!"}


# http://127.0.0.1:8000/posts
@app.get("/posts")
def read_post():
    return {"title": "my_post"}


# path parameters
# http://127.0.0.1:8000/posts/10
@app.get("/posts/{post_id}")
def read_post(post_id: int):
    return {"title": "unknown", "post_id": post_id}


# query parameters
# http://127.0.0.1:8000/search_sth?q=kot
@app.get('/search_sth')
def search(q: str):
    return {"result": f"ładny {q}"}


# http://127.0.0.1:8000/items?skip=5&limit20
@app.get('/items')
def get_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


# http://127.0.0.1:8000/users/10/posts?skip=15&limit=20
@app.get("/users/{user_id}/posts")
def get_user_posts(user_id: int, skip: int = 0, limit: int = 10):
    return {
        "user_id": user_id,
        "skip": skip,
        "limit": limit
    }
