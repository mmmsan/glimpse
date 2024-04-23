from config import settings
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from models import Users
from passlib.context import CryptContext
from pydantic import EmailStr    
from pytz import timezone
from sqlmodel import select, Session
import db


CRYPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/login"
)


async def auth(email: EmailStr, password: str):
    with Session(db.engine) as session:
        user = session.exec(select(Users).where(Users.email == email)).one()
        if not user:
            return None
        if not CRYPTO.verify(password, user.password):
            return None
        return user


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

