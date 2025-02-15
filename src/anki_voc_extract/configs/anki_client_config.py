from pydantic import Field

from anki_voc_extract.configs.base_config import BaseConfig


class AnkiClientConfig(BaseConfig):
    timeout: int = Field(default=30, description="Timeout for AnkiClient API calls")
