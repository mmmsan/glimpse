from pytz import timezone
from jose import JWTError, jwt
from config import settings
from datetime import datetime, timedelta
from models import Token, TokenData
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def generate_acess_token(user_id: str) -> str:
    return _create_token(
        token_type='access_token',
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        user_id=user_id
    )


def _create_token(token_type: str, lifetime: timedelta, user_id: str) -> str:
    tz = timezone('America/Cuiaba')
    expire = datetime.now(tz=tz) + lifetime
    payload = {}
    payload['user_id'] = user_id
    payload['type'] = token_type
    payload['exp'] = expire
    payload['iat'] = datetime.now(tz=tz)
    return jwt.encode(claims=payload, key=settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def verify_access_token(token: str = Depends(oauth2_scheme)) -> TokenData:

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f'Could not validate credentials',
                                          headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(token=token, key=settings.JWT_SECRET, algorithms=settings.ALGORITHM)
        user_id = payload.get("user_id")
        type = payload.get("type")
        exp = payload.get("exp")
        iat = payload.get("iat")
        if user_id or type or exp or iat is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id, type=type, exp=exp, iat=iat)
    except JWTError:
        raise credentials_exception

    return token_data
