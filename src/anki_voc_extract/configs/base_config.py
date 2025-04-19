from enum import Enum
from pathlib import Path
from typing import ClassVar, Type, TypeVar

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings

API_URL = "http://127.0.0.1:8765"


class BaseConfig(BaseSettings):
    """Base configuration class that all other configs should extend.

    Provides common settings and functionality for all configuration classes.
    """

    gemini_api_key: str | None = Field(
        default=None,
        description="Gemini API key for the Gemini API.",
    )
    ankiconnector_url: str = Field(
        default=API_URL,
        description="The url for AnkiConnector API",
    )
    model_config = ConfigDict(protected_namespaces=("settings_",))  # type: ignore

    # Class variable to store instances for the singleton pattern
    _instances: ClassVar[dict[Type["BaseConfig"], "BaseConfig"]] = {}

    @classmethod
    def get_instance(cls) -> "BaseConfig":
        """Get a singleton instance of this config class."""
        if cls not in cls._instances:
            cls._instances[cls] = cls()  # BaseSettings automatically loads from env
        return cls._instances[cls]


class AnkiClientConfig(BaseConfig):
    timeout: int = Field(default=30, description="Timeout for AnkiClient API calls")
    deck_name: str = Field(default="korean", description="Target anki deck")


class AvailableLang(str, Enum):
    ko = "ko"
    en = "en"
    ja = "ja"
    zh = "zh"


class AnkiTextCleanerConfig(BaseConfig):
    rm_mp3_path_flg: bool = Field(default=True, description="If remove the mp3 path text.")
    rm_html_path_flg: bool = Field(default=True, description="If remove the HTML tags.")
    target_lang: AvailableLang = Field(default=AvailableLang.ko, description="Target language for the text cleaner.")


class OutputterConfig(BaseConfig):
    output_path: Path = Field(default=Path("."), description="File path for the output file.")


T = TypeVar("T", bound=BaseConfig)


class ConfigFactory(BaseSettings):
    """Factory for creating and caching config instances."""

    @classmethod
    def get_config(cls, config_class: Type[T]) -> T:
        """Get the config instance.

        Returns:
            BaseConfig: BaseConfig instance.
        """
        # if cls._instances.get(cls):
        #     return cls._instances[cls]
        # else:
        #     cls._instances[cls] = cls()
        #     return cls._instances[cls]
        return config_class.get_instance()  # type: ignore

    @classmethod
    def get_anki_text_cleaner_config(cls) -> AnkiTextCleanerConfig:
        """Get the AnkiTextCleanerConfig instance.

        Returns:
            AnkiTextCleanerConfig: AnkiTextCleanerConfig instance.
        """
        return cls.get_config(AnkiTextCleanerConfig)

    @classmethod
    def get_anki_client_config(cls) -> AnkiClientConfig:
        """Get the AnkiClientConfig instance.

        Returns:
            AnkiClientConfig: AnkiClientConfig instance.
        """
        return cls.get_config(AnkiClientConfig)

    @classmethod
    def get_outputter_config(cls) -> OutputterConfig:
        """Get the OutputterConfig instance.

        Returns:
            OutputterConfig: OutputterConfig instance.
        """
        return cls.get_config(OutputterConfig)
