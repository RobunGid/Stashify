import logging

from pydantic import Field
from pydantic_settings import BaseSettings

logging.basicConfig(level=logging.INFO)


class Config(BaseSettings):
    token: str = Field(alias="TOKEN")

    postgres_user: str = Field(alias="POSTGRES_USER")
    postgres_password: str = Field(alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(alias="POSTGRES_DB")
    postgres_host: str = Field(default="localhost", alias="POSTGRES_HOST")
    postgres_port: int = Field(alias="POSTGRES_PORT")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}"
            f"/{self.postgres_db}"
        )

    @property
    def sync_database_url(self) -> str:
        return (
            f"postgresql://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@localhost:{self.postgres_port}"
            f"/{self.postgres_db}"
        )

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }
