from pytz import timezone
from jose import jwt
from config import settings
from datetime import datetime, timedelta


def generate_acess_token(subj: str) -> str:
    return _create_token(
        token_type='access_token',
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        subj=subj
    )


def _create_token(token_type: str, lifetime: timedelta, subj: str) -> str:
    tz = timezone('America/Cuiaba')
    expire = datetime.now(tz=tz) + lifetime
    payload = {}
    payload['type'] = token_type
    payload['exp'] = expire
    payload['iat'] = datetime.now(tz=tz)
    payload['subj'] = subj
    return jwt.encode(claims=payload, key=settings.JWT_SECRET, algorithm=settings.ALGORITHM)
