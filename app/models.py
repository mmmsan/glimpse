from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel 


class PostBase(SQLModel):
    title: str
    content: str
    created_at: Optional[datetime] = Field(default=datetime.now())


class Posts(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int


# ---


class UserBase(SQLModel):
    email: str = Field(unique=True)
    password: str
    created_at: Optional[datetime] = Field(default=datetime.now())


class Users(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
