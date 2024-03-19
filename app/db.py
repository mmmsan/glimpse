from sqlmodel import SQLModel, create_engine

db_url = 'postgresql+psycopg2://marcos:postgres@localhost/glimpse'
engine = create_engine(db_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


