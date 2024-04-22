from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from fastapi import status, HTTPException, APIRouter
from sqlmodel import Session, desc
import utils
import models
import db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{id}", 
            summary='busca um usuario especifico',
            description='',
            response_description='',
            response_model=models.UserResponse)
async def read_user_id(id: int):
    with Session(db.engine) as session:
        user = session.get(models.Users, id)
        if not user:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"User with id {id} was not found.",
            )
        else:
            return user


@router.post(
    "/", 
    summary='cria um usuario',
    description='',
    response_description='',
    status_code=status.HTTP_201_CREATED, response_model=models.UserResponse
)
async def create_user(user: models.Users):
    user.password = utils.hash(user.password)
    with Session(db.engine) as session:
        new_user = models.Users(email=user.email, password=user.password)
        try:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
        except:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail=f"E-mail already in use."
            )
    return new_user
