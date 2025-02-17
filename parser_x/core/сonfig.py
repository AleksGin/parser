from pathlib import Path

from pydantic import (
    BaseModel,
    PostgresDsn,
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class AppRunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class DataBaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 50


class SpimexConfig(BaseModel):
    results_url: str
    upload_url: str
    path_to_folder: Path


class Config(BaseSettings):
    DB_Config: DataBaseConfig
    SPX_Config: SpimexConfig

    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


settings = Config()
