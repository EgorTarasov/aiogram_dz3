from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
    )
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int = 5432

    redis_host: str
    redis_port: int = 6379

    bot_token: str


config = Config()

#     POSTGRES_USER = pguser


# POSTGRES_PASSWORD = pgpassword
# POSTGRES_DB = dev
# POSTGRES_HOST = localhost
# POSTGRES_PORT = 5432


# REDIS_HOST = localhost
# REDIS_PORT = 6379
