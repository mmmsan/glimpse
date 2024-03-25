from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from typing import List
from fastapi import APIRouter, status, HTTPException
from sqlmodel import Session, select
from .. import db, models 

router = APIRouter()


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=models.PostCreate)
def create_post(post: models.Posts):
    with Session(db.engine) as session:
        new_post = models.Posts(title=post.title, content=post.content)
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
    return new_post


@router.get("/posts", response_model=List[models.PostRead])
def read_posts():
    with Session(db.engine) as session:
        posts = session.exec(select(models.Posts)).all()
    return posts


@router.get("/posts/{id}", response_model=models.PostRead)
def read_posts_id(id: int):
    with Session(db.engine) as session:
        post = session.get(models.Posts, id)
    if not post:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'Post with id {id} was not found.')
    else:
        return post


@router.put("/posts/{id}")
def update_post(id: int, new_post: models.PostRead):
    old_post = read_posts_id(id)
    with Session(db.engine) as session:
        old_post.title = new_post.title
        old_post.content = new_post.content
        session.add(old_post)
        session.commit()
        session.refresh(old_post)
    return old_post
        

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = read_posts_id(id)
    with Session(db.engine) as session:
        session.delete(post)
        session.commit()
