from . import database
from . import models
from starlette.status import HTTP_404_NOT_FOUND
from typing import List
from fastapi import FastAPI, status, HTTPException
from sqlmodel import Session, select

app = FastAPI()


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: models.Posts):
    with Session(database.engine) as session:
        new_post = models.Posts(title=post.title, content=post.content)
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
    return new_post


@app.get("/posts", response_model=List[models.Posts])
def read_posts():
    with Session(database.engine) as session:
        posts = session.exec(select(models.Posts)).all()
    return posts


@app.get("/posts/{id}", response_model=models.Posts)
def read_posts_id(id: int):
    with Session(database.engine) as session:
        post = session.get(models.Posts, id)
    if not post:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'Post with id {id} was not found.')
    else:
        return post


@app.put("/posts/{id}")
def update_post(id: int, new_post: models.Posts):
    old_post = read_posts_id(id)
    with Session(database.engine) as session:
        old_post.title = new_post.title
        old_post.content = new_post.content
        session.add(old_post)
        session.commit()
        session.refresh(old_post)
    return old_post
        

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = read_posts_id(id)
    with Session(database.engine) as session:
        session.delete(post)
        session.commit()
