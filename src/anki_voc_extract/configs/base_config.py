from pydantic import Field
from pydantic_settings import BaseSettings

API_URL = "http://127.0.0.1:8765"


class BaseConfig(BaseSettings):
    """Common config for all the config modules.

    Args:
        BaseSettings (_type_): _description_
    """

    ankiconnector_url: str = Field(
        default=API_URL,
        description="The url for AnkiConnector API",
    )

    deck_name: str = Field(default="korean", description="Target anki deck")
