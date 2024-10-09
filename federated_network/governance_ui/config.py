from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    pysyft_url: str
    pysyft_port: str
    fusionauth_api_key: str
    fusionauth_client_id: str
    fusionauth_client_secret: str
    oauth_provider_auth_url: str
    oauth_provider_app_url: str

    blockchain_api_url: str

    pysyft_root_user_email: Optional[str] = "info@openmined.org"
    pysyft_root_user_password: Optional[str] = "changethis"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)


config = Settings()
