from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from fastapi import status, HTTPException, APIRouter
from sqlmodel import Session
from .. import db, models, utils

router = APIRouter()


@router.get('/users/{id}', response_model=models.UserResponse)
def read_user_id(id: int):
    with Session(db.engine) as session:
        user = session.get(models.Users, id)
        if not user:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'User with id {id} was not found.')
        else:
            return user


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=models.UserResponse)
def create_user(user: models.Users):
    user.password = utils.hash(user.password)
    with Session(db.engine) as session:
        new_user = models.Users(email=user.email, password=user.password)
        try:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
        except:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=f'E-mail already in use.')
    return new_user
