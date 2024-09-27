import time
import psycopg2
from psycopg2.extras import RealDictCursor 
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

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

class Post(BaseModel):
    title: str
    content: str

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *""",
        (post.title, post.content)
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {'data': new_post}


@app.get("/posts")
def read_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {'data': posts}


@app.get("/posts/{id}")
def read_posts_id(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} was not found')
    return {'data': post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
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
    return {'data': updated_post}
        

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} was not found')
    return {'message': 'Post with id {id} has been deleted'}
