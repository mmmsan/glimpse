import time
import psycopg2
from psycopg2.extras import RealDictCursor 
from fastapi import FastAPI, status, HTTPException
from . import schemas
from typing import List

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(
            host='localhost', 
            database='webapp', 
            user='postgres', 
            password='',
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print('=== DB connected ===')
        break
    except Exception as e:
        print('=== Connection to DB failed ===')
        time.sleep(5)

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostBase)
def create_post(post: schemas.PostBase):
    cursor.execute(
        """INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *""",
        (post.title, post.content)
    )
    new_post = cursor.fetchone()
    conn.commit()
    return new_post


@app.get("/posts", response_model=List[schemas.PostBase])
def read_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return posts


@app.get("/posts/{id}", response_model=schemas.PostBase)
def read_posts_id(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} was not found')
    return post


@app.put("/posts/{id}", response_model=schemas.PostBase)
def update_post(id: int, post: schemas.PostBase):
    cursor.execute(
        """
        UPDATE posts
        SET title = %s, content = %s
        WHERE id = %s
        RETURNING *
        """,
        (post.title, post.content, str(id))
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} was not found')
    return updated_post
        

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} was not found')
    return {'message': 'Post with id {id} has been deleted'}
