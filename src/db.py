from sqlalchemy.engine.interfaces import DBAPIType
from sqlmodel import SQLModel, create_engine
from config import settings


engine = create_engine(settings.DB_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
