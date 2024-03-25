from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from typing import List
from fastapi import FastAPI, status, HTTPException
from sqlmodel import Session, select
from .db import *
from .models import *
from .utils import *

app = FastAPI()

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostCreate)
def create_post(post: Posts):
    with Session(engine) as session:
        new_post = Posts(title=post.title, content=post.content)
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
    return new_post


@app.get("/posts", response_model=List[PostRead])
def read_posts():
    with Session(engine) as session:
        posts = session.exec(select(Posts)).all()
    return posts


@app.get("/posts/{id}", response_model=PostRead)
def read_posts_id(id: int):
    with Session(engine) as session:
        post = session.get(Posts, id)
    if not post:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'Post with id {id} was not found.')
    else:
        return post


@app.put("/posts/{id}")
def update_post(id: int, new_post: PostRead):
    old_post = read_posts_id(id)
    with Session(engine) as session:
        old_post.title = new_post.title
        old_post.content = new_post.content
        session.add(old_post)
        session.commit()
        session.refresh(old_post)
    return old_post
        

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = read_posts_id(id)
    with Session(engine) as session:
        session.delete(post)
        session.commit()


# ---


@app.get('/users/{id}', response_model=UserResponse)
def read_user_id(id: int):
    with Session(engine) as session:
        user = session.get(Users, id)
        if not user:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'User with id {id} was not found.')
        else:
            return user


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: Users):
    user.password = hash(user.password)
    with Session(engine) as session:
        new_user = Users(email=user.email, password=user.password)
        try:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
        except:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=f'E-mail already in use.')
    return new_user



# --- 


def main():
    create_db_and_tables()


if __name__ == "__main__":
    main()
