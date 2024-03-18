from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    amqp_url: str = "amqp://guest:guest@localhost:8008/"
    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
