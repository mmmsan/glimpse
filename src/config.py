from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "postgresql+psycopg2://postgres:123@localhost/glimpse"
    JWT_SECRET: str = "EcDt1zAurlT3bSmZcMWCjHSFNvPb3rosPTcc6WlmIQk"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7


settings = Settings()
