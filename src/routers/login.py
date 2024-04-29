from config import CRYPTO
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from models import Users
from sqlmodel import select, Session
from auth import generate_acess_token
import db

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(cred: OAuth2PasswordRequestForm = Depends()):
    with Session(db.engine) as session:
        user = session.exec(select(Users).where(Users.email == cred.username)).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Invalid credentials')
        if not CRYPTO.verify(cred.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid credentials')
    access_token = generate_acess_token(user_id=user.id)
    return {"access_token": access_token, "token_type": "bearer"}


