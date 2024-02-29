from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class Posts(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
