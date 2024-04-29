from typing import Optional
from datetime import datetime
from sqlalchemy.sql.roles import SQLRole
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


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, sa_type=AutoString)
    created_at: Optional[datetime] = Field(default=datetime.now())


class Users(UserBase, table=True):
    password: str
    id: Optional[int] = Field(default=None, primary_key=True)


class UserResponse(UserBase):
    id: int
    pass


#class UserLogin(SQLModel):
#    email: EmailStr
#    password: str


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    user_id: int
    type: str
    exp: datetime
    iat: datetime
