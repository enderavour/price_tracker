from pydantic_settings import SettingsConfigDict, BaseSettings

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    algolia_app_id: str
    algolia_api_key: str
    algolia_app_url: str = "https://tgk4nzb4wl-dsn.algolia.net/1/indexes/*/queries"

settings = Settings()