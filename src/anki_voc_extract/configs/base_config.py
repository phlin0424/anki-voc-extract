from enum import Enum
from pathlib import Path
from typing import ClassVar, TypeVar

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings

API_URL = "http://127.0.0.1:8765"

# ===========================================================
# Base configuration class
# ===========================================================


class BaseConfig(BaseSettings):
    """Base configuration class that all other configs should extend.

    Provides common settings and functionality for all configuration classes.
    """

    model_config = ConfigDict(protected_namespaces=("settings_",))  # type: ignore

    # Class variable to store instances for the singleton pattern
    _instances: ClassVar[dict[type["BaseConfig"], "BaseConfig"]] = {}

    @classmethod
    def get_instance(cls) -> "BaseConfig":
        """Get a singleton instance of this config class."""
        if cls not in cls._instances:
            cls._instances[cls] = cls()  # BaseSettings automatically loads from env
        return cls._instances[cls]


# ===========================================================
# Configuration classes for AnkiClient
# ===========================================================


class AnkiClientConfig(BaseConfig):
    ankiconnector_url: str = Field(
        default=API_URL,
        description="The url for AnkiConnector API",
    )
    timeout: int = Field(default=30, description="Timeout for AnkiClient API calls")
    deck_name: str = Field(default="korean", description="Target anki deck")


# ===========================================================
# Configuration classes for AnkiTextCleaner
# ===========================================================


class AvailableLang(str, Enum):
    ko = "ko"
    en = "en"
    ja = "ja"
    zh = "zh"


class AnkiTextCleanerConfig(BaseConfig):
    rm_mp3_path_flg: bool = Field(default=True, description="If remove the mp3 path text.")
    rm_html_path_flg: bool = Field(default=True, description="If remove the HTML tags.")
    target_lang: AvailableLang = Field(default=AvailableLang.ko, description="Target language for the text cleaner.")


# ===========================================================
# Configuration classes for AI agent
# ===========================================================


class AIAgentConfig(BaseConfig):
    """Configuration for AI Agent."""

    model_name: str = Field(default="gemini-pro", description="Model name to use with the provider")
    gemini_api_key: str = Field(default="", description="API key for the AI provider")
    gemini_model_name: str = Field(
        default="gemini-2.0-flash-001",
        description="Model name for Gemini API. Default is 'gemini-2.0-flash-001'.",
    )
    project: None | str = Field(
        default=None,
        description="Project ID for Gemini API. Default is 'be-lin-pei-hsuan'.",
    )
    location: None | str = Field(
        default=None,
        description="Location for Gemini API. Default is 'us-central1'.",
    )


# ===========================================================
# Configuration classes for Outputter
# ===========================================================


class OutputterConfig(BaseConfig):
    output_path: Path = Field(default=Path(), description="File path for the output file.")


# ===========================================================
# Factory for creating and caching config instances
# ===========================================================

T = TypeVar("T", bound=BaseConfig)


class ConfigFactory(BaseSettings):
    """Factory for creating and caching config instances."""

    @classmethod
    def get_config(cls, config_class: type[T]) -> T:
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

    @classmethod
    def get_ai_agent_config(cls) -> AIAgentConfig:
        """Get the AIAgentConfig instance.

        Returns:
            AIAgentConfig: AIAgentConfig instance.
        """
        return cls.get_config(AIAgentConfig)
