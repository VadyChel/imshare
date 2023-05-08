from pydantic import BaseSettings, PostgresDsn, BaseModel


class App(BaseModel):
    port: int = 8080
    host: str = 'localhost'
    reload: bool = True
    proxy_headers: bool = False


class Config(BaseSettings):
    app: App
    database_url: PostgresDsn
    max_name_length: int | None = 32
    max_file_length: int | None = 500_000  # 500kb

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


config = Config()
