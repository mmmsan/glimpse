from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, AutoString
from pydantic import EmailStr


class PostBase(SQLModel):
    title: str
    content: str
    created_at: Optional[datetime] = Field(default=datetime.now())


class Posts(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    pass


# ---


class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, sa_type=AutoString)
    password: str
    created_at: Optional[datetime] = Field(default=datetime.now())


class UserResponse(SQLModel):
    id: int
    email: EmailStr
    created_at: Optional[datetime] = Field(default=datetime.now())
