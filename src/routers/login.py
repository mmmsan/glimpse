from config import CRYPTO
from fastapi import APIRouter, status, HTTPException
from models import Users, UserLogin
from sqlmodel import select, Session
from auth import generate_acess_token
import db

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(cred: UserLogin):
    with Session(db.engine) as session:
        user = session.exec(select(Users).where(Users.email == cred.email)).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid credentials')
        if not CRYPTO.verify(cred.password, user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid credentials')
    access_token = generate_acess_token(subj='usuario')
    return {"access_token": access_token, "token_type": "bearer"}


