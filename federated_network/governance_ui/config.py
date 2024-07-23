from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    pysyft_url: str
    pysyft_port: str
    fusionauth_api_key: str
    fusionauth_client_id: str
    fusionauth_client_secret: str
    oauth_provider_auth_url: str
    oauth_provider_app_url: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)


config = Settings()
