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
    id: int
    pass


# ---


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, sa_type=AutoString)
    created_at: Optional[datetime] = Field(default=datetime.now())


class Users(UserBase, table=True):
    password: str
    id: Optional[int] = Field(default=None, primary_key=True)


class UserResponse(UserBase):
    pass
