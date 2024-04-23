from fastapi import FastAPI
from models import *
from db import create_db_and_tables
from routers import posts, users, auth

app = FastAPI(title="glimpse API", version="0.4.0")
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


def main():
    create_db_and_tables()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
