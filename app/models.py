from typing import Optional
from sqlmodel import Field, SQLModel


class PostBase(SQLModel):
    title: str
    content: str


class Posts(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    pass

