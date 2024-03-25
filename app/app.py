from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from typing import List
from fastapi import FastAPI, status, HTTPException
from sqlmodel import Session, select
from . import models
from .db import create_db_and_tables
from .routers import posts, users

app = FastAPI()
app.include_router(posts.router)
app.include_router(users.router)


def main():
    create_db_and_tables()


if __name__ == "__main__":
    main()
