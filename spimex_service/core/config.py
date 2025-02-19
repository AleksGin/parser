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


class Config(BaseSettings):
    DB_Config: DataBaseConfig
    AppConfig: AppRunConfig = AppRunConfig()

    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


settings = Config()
