from pydantic import Field
from pydantic_settings import BaseSettings

API_URL = "http://127.0.0.1:8765"


class Config(BaseSettings):
    api_url: str = Field(
        default=API_URL,
        description="The url for AnkiConnector API",
    )
