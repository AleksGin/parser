from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DataBaseConfig(BaseModel):
    name: str
    host: str
    port: int
    user: str
    password: str
    
    
class SpimexConfig(BaseModel):
    url: str


class Config(BaseSettings):
    DB_Config: DataBaseConfig
    SPX_Config: SpimexConfig

    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


settings = Config()
