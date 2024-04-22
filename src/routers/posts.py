from starlette.status import HTTP_404_NOT_FOUND
from typing import List
from fastapi import APIRouter, status, HTTPException
from sqlmodel import Session, select
import models
import db

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", 
             summary='cria um novo post',
             description='',
             status_code=status.HTTP_201_CREATED, 
             response_description='',
             response_model=models.PostCreate)
async def create_post(post: models.Posts):
    with Session(db.engine) as session:
        new_post = models.Posts(title=post.title, content=post.content)
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
    return new_post


@router.get("/", 
            summary='busca todos os posts',
            response_description='',
            description='',
            response_model=List[models.PostRead])
async def read_posts():
    with Session(db.engine) as session:
        posts = session.exec(select(models.Posts)).all()
    return posts


@router.get("/{id}", 
            summary='busca um post especifico',
            description='',
            response_description='',
            response_model=models.PostRead)
async def read_posts_id(id: int):
    with Session(db.engine) as session:
        post = session.get(models.Posts, id)
    if not post:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found."
        )
    else:
        return post


@router.put("/{id}",
            summary='atualiza um post especifico',
            response_description='atualizado com sucesso',
            description='',
            )
async def update_post(id: int, new_post: models.PostRead):
    old_post = read_posts_id(id)
    with Session(db.engine) as session:
        old_post.title = new_post.title
        old_post.content = new_post.content
        session.add(old_post)
        session.commit()
        session.refresh(old_post)
    return old_post


@router.delete("/{id}", 
               summary='deleta um post especifico',
               description='',
               response_description='deletado com sucesso',
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    post = read_posts_id(id)
    with Session(db.engine) as session:
        session.delete(post)
        session.commit()
