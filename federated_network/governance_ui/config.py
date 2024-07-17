from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    pysyft_url: str = Field(..., env="PYSYFT_URL")
    pysyft_port: str = Field(..., env="PYSYFT_PORT")
    fusionauth_client_id: str = Field(..., env="FUSIONAUTH_CLIENT_ID")
    fusionauth_client_secret: str = Field(..., env="FUSIONAUTH_CLIENT_SECRET")
    oauth_provider_auth_url: str = Field(..., env="OAUTH_PROVIDER_AUTH_URL")
    oauth_provider_app_url: str = Field(..., env="OAUTH_PROVIDER_APP_URL")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


config = Settings()
