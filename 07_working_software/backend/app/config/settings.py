"""Application settings loaded from environment variables (.env)."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "AI Knowledge Discovery & Decision Assistant"
    environment: str = "development"

    database_url: str = "sqlite:///./data/app.db"

    chroma_host: str = "localhost"
    chroma_port: int = 8001
    chroma_collection_name: str = "knowledge_base"

    openai_api_key: str = ""
    openai_base_url: str = ""  # non-empty to route through an internal gateway (e.g. https://genailab.tcs.in/v1)
    openai_verify_ssl: bool = True  # some internal gateways sit behind a proxy with a self-signed cert
    openai_chat_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    use_azure_openai: bool = False
    azure_openai_endpoint: str = ""
    azure_openai_api_version: str = "2024-02-01"

    jwt_secret_key: str = "change-me-in-production"
    cors_allow_origins: list[str] = ["http://localhost:5173"]

    storage_path: str = "./data/documents"


@lru_cache
def get_settings() -> Settings:
    return Settings()
