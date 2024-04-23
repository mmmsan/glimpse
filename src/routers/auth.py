from starlette.types import HTTPExceptionHandler
from config import settings
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, status, HTTPException, Response
from jose import jwt
from models import Users, UserLogin
from config import CRYPTO
from pydantic import EmailStr    
from pytz import timezone
from sqlmodel import select, Session
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
        #return user
        return {"login": "Successfully logged in"}


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/login"
)


def _create_token(token_type: str, lifetime: timedelta, subj: str) -> str:
    tz = timezone('America/Cuiada')
    expire = datetime.now(tz=tz) + lifetime

    payload = {}
    payload['type'] = token_type
    payload['exp'] = expire
    payload['iat'] = datetime.now(tz=tz)
    payload['subj'] = subj

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def generate_acess_token(subj: str) -> str:
    return _create_token(
        token_type='access_token',
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        subj=subj
    )

